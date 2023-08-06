import os
import sys
import traceback
from functools import wraps
from textwrap import dedent

import click

from dennis import __version__
from dennis.linter import Linter
from dennis.minisix import PY2, textclass
from dennis.templatelinter import TemplateLinter
from dennis.tools import (
    FauxTerminal,
    Terminal,
    get_available_vars,
    parse_pofile,
    withlines
)
from dennis.translator import Translator, get_available_pipeline_parts


USAGE = '%prog [options] [command] [command-options]'
VERSION = 'dennis ' + __version__

# blessings.Terminal and our FauxTerminal don't maintain any state so
# we can make it global
if sys.stdout.isatty():
    TERM = Terminal()
else:
    TERM = FauxTerminal()


def utf8_args(fun):
    @wraps(fun)
    def _utf8_args(*args):
        args = [part.encode('utf-8') for part in args]
        return fun(*args)
    return _utf8_args


def out(*s):
    for part in s:
        click.echo(part, nl=False)
    click.echo('')


def err(*s):
    """Prints a single-line string to stderr."""
    parts = [
        TERM.bold_red,
        'Error: '
    ]
    parts.extend(s)
    parts.append(TERM.normal)
    for part in parts:
        click.echo(part, nl=False, err=True)
    click.echo('')


if PY2 and not sys.stdout.isatty():
    # If it's Python2 and not a tty, then we need to encode the text
    # type things as utf8 before spitting them out to stdout and
    # stderr.
    out = utf8_args(out)
    err = utf8_args(err)


def format_vars():
    vars_ = sorted(get_available_vars().items())
    lines = [
        'Available Variable Formats:',
        '',
        '\b',
    ]
    lines.extend(
        ['{name:13}  {desc}'.format(name=name, desc=cls.desc)
         for name, cls in vars_]
    )

    text = '\n'.join(lines) + '\n'
    return text


def format_pipeline_parts():
    parts = sorted(get_available_pipeline_parts().items())
    lines = [
        'Available Pipeline Parts:',
        '',
        '\b',
    ]
    lines.extend(
        ['{name:13}  {desc}'.format(name=name, desc=cls.desc)
         for name, cls in parts]
    )
    text = '\n'.join(lines) + '\n'
    return text


def format_lint_rules():
    from dennis.linter import get_available_lint_rules
    rules = sorted(get_available_lint_rules().items())
    lines = [
        'Available Lint Rules:',
        '',
        '\b',
    ]
    lines.extend(
        ['{num:6} {name}: {desc}'.format(num=num, name=cls.name,
                                         desc=cls.desc)
         for num, cls in rules]
    )
    text = '\n'.join(lines) + '\n'
    return text


def format_lint_template_rules():
    from dennis.templatelinter import get_available_lint_rules
    rules = sorted(get_available_lint_rules().items())
    lines = [
        'Available Template Lint Rules:',
        '',
        '\b',
    ]
    lines.extend(
        ['{num:6} {name}: {desc}'.format(num=num, name=cls.name,
                                         desc=cls.desc)
         for num, cls in rules]
    )
    text = '\n'.join(lines) + '\n'
    return text


def epilog(docstring):
    """Fixes the docstring so it displays properly

    I have problems with docstrings and indentation showing up right
    in click. This fixes that. Plus it allows me to add dynamically
    generated bits to the docstring.

    """
    def _epilog(fun):
        fun.__doc__ = dedent(fun.__doc__) + docstring
        return fun
    return _epilog


def click_run():
    sys.excepthook = exception_handler
    cli(obj={})


@click.group()
def cli():
    pass


@cli.command()
@click.option('--quiet/--no-quiet', default=False)
@click.option('--color/--no-color', default=True)
@click.option('--varformat', default='pysprintf,pyformat',
              help=('Comma-separated list of variable types. '
                    'See Available Variable Formats.'))
@click.option('--rules', default='',
              help=('Comma-separated list of lint rules to use. '
                    'Defaults to all rules. See Available Lint Rules.'))
@click.option('--reporter', default='',
              help='Reporter to use for output.')
@click.option('--errorsonly/--no-errorsonly', default=False,
              help='Only print errors.')
@click.argument('path', nargs=-1)
@click.pass_context
@epilog(format_vars() + '\n' +
        format_lint_rules() + '\n' +
        format_lint_template_rules())
def lint(ctx, quiet, color, varformat, rules, reporter, errorsonly, path):
    """
    Lints .po/.pot files for issues

    You can ignore rules on a string-by-string basis by adding an
    extracted comment "dennis-ignore: <comma-separated-rules>".  See
    documentation for details.

    """
    global TERM

    if not quiet:
        out('dennis version {version}'.format(version=__version__))

    if not color:
        TERM = FauxTerminal()

    linter = Linter(varformat.split(','), rules.split(','))
    templatelinter = TemplateLinter(varformat.split(','),
                                    rules.split(','))

    po_files = []
    for item in path:
        if os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                po_files.extend(
                    [os.path.join(root, fn) for fn in files
                     if fn.endswith(('.po', '.pot'))])
        else:
            po_files.append(item)

    po_files = [os.path.abspath(fn) for fn in po_files
                if fn.endswith(('.po', '.pot'))]

    if not po_files:
        err('Nothing to work on.')
        ctx.exit(1)

    files_to_errors = {}
    total_error_count = 0
    total_warning_count = 0
    total_files_with_errors = 0

    for fn in po_files:
        try:
            if not os.path.exists(fn):
                raise IOError('File "{fn}" does not exist.'.format(fn=fn))

            if fn.endswith('.po'):
                results = linter.verify_file(fn)
            else:
                results = templatelinter.verify_file(fn)
        except IOError as ioe:
            # This is not a valid .po file. So mark it as an error.
            err('>>> Problem opening file: {fn}'.format(fn=fn))
            err(repr(ioe))
            out('')

            # FIXME - should we track this separately as an invalid
            # file?
            files_to_errors[fn] = (1, 0)
            total_error_count += 1
            continue

        if errorsonly:
            # Go through and nix all the non-error LintMessages
            results = [res for res in results if res.kind == 'err']

        # We don't want to print output for files that are fine, so we
        # update the bookkeeping and move on.
        if not results:
            files_to_errors[fn] = (0, 0)
            continue

        if not quiet and not reporter:
            out(TERM.bold_green,
                '>>> Working on: {fn}'.format(fn=fn),
                TERM.normal)

        error_results = [res for res in results if res.kind == 'err']
        warning_results = [res for res in results if res.kind == 'warn']

        error_count = len(error_results)
        total_error_count += error_count

        warning_count = len(warning_results)
        total_warning_count += warning_count

        if not quiet:
            for msg in error_results:
                if reporter == 'line':
                    out(fn,
                        ':',
                        textclass(msg.poentry.linenum),
                        ':',
                        '0',
                        ':',
                        msg.code,
                        ':',
                        msg.msg)
                else:
                    out(TERM.bold_red,
                        msg.code,
                        ': ',
                        msg.msg,
                        TERM.normal)
                    out(withlines(msg.poentry.linenum, msg.poentry.original))
                    out('')

        if not quiet and not errorsonly:
            for msg in warning_results:
                if reporter == 'line':
                    out(fn,
                        ':',
                        textclass(msg.poentry.linenum),
                        ':',
                        '0',
                        ':',
                        msg.code,
                        ':',
                        msg.msg)
                else:
                    out(TERM.bold_yellow,
                        msg.code,
                        ': ',
                        msg.msg,
                        TERM.normal)
                    out(withlines(msg.poentry.linenum, msg.poentry.original))
                    out('')

        files_to_errors[fn] = (error_count, warning_count)

        if error_count > 0:
            total_files_with_errors += 1

        if not quiet and reporter != 'line':
            out('Totals')
            if not errorsonly:
                out('  Warnings: {warnings:5}'.format(warnings=warning_count))
            out('  Errors:   {errors:5}\n'.format(errors=error_count))

    if len(po_files) > 1 and not quiet and reporter != 'line':
        out('Final totals')
        out('  Number of files examined:          {count:5}'.format(
            count=len(po_files)))
        out('  Total number of files with errors: {count:5}'.format(
            count=total_files_with_errors))
        if not errorsonly:
            out('  Total number of warnings:          {count:5}'.format(
                count=total_warning_count))
        out('  Total number of errors:            {count:5}'.format(
            count=total_error_count))
        out('')

        file_counts = [
            (counts[0], counts[1], fn.split(os.sep)[-3], fn.split(os.sep)[-1])
            for (fn, counts) in files_to_errors.items()
        ]

        # If we're showing errors only, then don't talk about warnings.
        if errorsonly:
            header = 'Errors  Filename'
            line = ' {errors:5}  {locale} ({fn})'
        else:
            header = 'Warnings  Errors  Filename'
            line = '   {warnings:5}   {errors:5}  {locale} ({fn})'

        file_counts = list(reversed(sorted(file_counts)))
        printed_header = False
        for error_count, warning_count, locale, fn in file_counts:
            if not error_count and not warning_count:
                continue
            if not printed_header:
                out(header)
                printed_header = True

            out(line.format(
                warnings=warning_count, errors=error_count, fn=fn,
                locale=locale))

    # Return 0 if everything was fine or 1 if there were errors.
    ctx.exit(code=1 if total_error_count else 0)


@cli.command()
@click.option('--showuntranslated', is_flag=True, default=False,
              help='Show untranslated strings')
@click.argument('path', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def status(ctx, showuntranslated, path):
    """Show status of a .po file."""
    out('dennis version {version}'.format(version=__version__))

    po_files = []
    for item in path:
        if os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                po_files.extend(
                    [os.path.join(root, fn) for fn in files
                     if fn.endswith('.po')])
        else:
            po_files.append(item)

    po_files = [os.path.abspath(fn) for fn in po_files
                if fn.endswith('.po')]

    for fn in po_files:
        try:
            if not os.path.exists(fn):
                raise IOError('File "{fn}" does not exist.'.format(fn=fn))

            pofile = parse_pofile(fn)
        except IOError as ioe:
            err('>>> Problem opening file: {fn}'.format(fn=fn))
            err(repr(ioe))
            continue

        out('')
        out(TERM.bold_green, '>>> Working on: {fn}'.format(fn=fn), TERM.normal)

        out('Metadata:')
        for key in ('Language', 'Report-Msgid-Bugs-To', 'PO-Revision-Date',
                    'Last-Translator', 'Language-Team', 'Plural-Forms'):
            if key in pofile.metadata and pofile.metadata[key]:
                out('  ', key, ': ', pofile.metadata[key])
        out('')

        if showuntranslated:
            out('Untranslated strings:')
            out('')
            for poentry in pofile.untranslated_entries():
                out(withlines(poentry.linenum, poentry.original))
                out('')

        out('Statistics:')
        out('  # Translated:   {0}'.format(len(pofile.translated_entries())))
        out('  # Fuzzy:        {0}'.format(len(pofile.fuzzy_entries())))
        out('  # Untranslated: {0}'.format(len(pofile.untranslated_entries())))
        if pofile.percent_translated() == 100:
            out('  Percentage:     100% COMPLETE!')
        else:
            out('  Percentage:     {0}%'.format(pofile.percent_translated()))
    ctx.exit(0)


@cli.command()
@click.option('--varformat', default='pysprintf,pyformat',
              help=('Comma-separated list of variable types. '
                    'See Available Variable Formats.'))
@click.option('--pipeline', '-p', default='html,pirate',
              help=('Comma-separated translate pipeline. See Available '
                    'Pipeline Parts.'))
@click.option('--strings', '-s', default=False, is_flag=True,
              help='Command line args are strings to be translated')
@click.argument('path', nargs=-1)
@click.pass_context
@epilog(format_vars() + '\n' +
        format_pipeline_parts())
def translate(ctx, varformat, pipeline, strings, path):
    """
    Translate a single string or .po file of strings.

    If you want to pull the string from stdin, use "-".

    Note: Translating files is done in-place replacing the original
    file.

    """
    if not (len(path) == 1 and path[0] == '-'):
        out('dennis version {version}'.format(version=__version__))

    if not path:
        err('Nothing to work on.')
        ctx.exit(1)

    translator = Translator(
        varformat.split(','), pipeline.split(','))

    if strings:
        # Args are strings to be translated
        for arg in path:
            data = translator.translate_string(arg)
            if PY2:
                data = data.encode('utf-8')
            out(data)

    elif len(path) == 1 and path[0] == '-':
        # Read everything from stdin, then translate it
        data = click.get_binary_stream('stdin').read()
        data = translator.translate_string(data)
        out(data)

    else:
        # Args are filenames
        for arg in path:
            translator.translate_file(arg)

    ctx.exit(0)


def exception_handler(exc_type, exc_value, exc_tb):
    click.echo('Oh no! Dennis has thrown an error while trying to do stuff.')
    click.echo('Please write up a bug report with the specifics so that ')
    click.echo('we can fix it.')
    click.echo('')
    click.echo('https://github.com/willkg/dennis/issues')
    click.echo('')
    click.echo('Here is some information you can copy and paste into the ')
    click.echo('bug report:')
    click.echo('')
    click.echo('---')
    out('Dennis: ', repr(__version__))
    out('Python: ', repr(sys.version))
    out('Command line: ', repr(sys.argv))
    click.echo(
        ''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    click.echo('---')

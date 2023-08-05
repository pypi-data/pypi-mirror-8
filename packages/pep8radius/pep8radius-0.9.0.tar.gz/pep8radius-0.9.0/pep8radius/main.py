"""This module does the argument and config parsing, and contains the main
function (that is called when calling pep8radius from shell)."""

from __future__ import print_function

import os
import sys

from argparse import ArgumentParser
try:
    from ConfigParser import SafeConfigParser, NoSectionError
except ImportError:  # py3, pragma: no cover
    from configparser import SafeConfigParser, NoSectionError

from pep8radius.radius import Radius
from pep8radius.shell import CalledProcessError  # with 2.6 compat

__version__ = version = '0.9.0'


DEFAULT_IGNORE = 'E24'
DEFAULT_INDENT_SIZE = 4

if sys.platform == 'win32':  # pragma: no cover
    DEFAULT_CONFIG = os.path.expanduser(r'~\.pep8')
else:
    DEFAULT_CONFIG = os.path.join(os.getenv('XDG_CONFIG_HOME') or
                                  os.path.expanduser('~/.config'), 'pep8')
PROJECT_CONFIG = ('setup.cfg', 'tox.ini', '.pep8')


def main(args=None, vc=None, cwd=None, apply_config=False):
    """PEP8 clean only the parts of the files touched since the last commit, a
    previous commit or branch."""
    import signal

    try:  # pragma: no cover
        # Exit on broken pipe.
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:  # pragma: no cover
        # SIGPIPE is not available on Windows.
        pass

    try:
        if args is None:
            args = []

        try:
            # Note: argparse on py 2.6 you can't pass a set
            # TODO neater solution for this!
            args_set = set(args)
        except TypeError:
            args_set = args  # args is a Namespace
        if '--version' in args_set or getattr(args_set, 'version', 0):
            print(version)
            sys.exit(0)
        if '--list-fixes' in args_set or getattr(args_set, 'list_fixes', 0):
            from autopep8 import supported_fixes
            for code, description in sorted(supported_fixes()):
                print('{code} - {description}'.format(
                    code=code, description=description))
            sys.exit(0)

        try:
            try:
                args = parse_args(args, apply_config=apply_config)
            except TypeError:
                pass  # args is already a Namespace (testing)
            r = Radius(rev=args.rev, options=args, vc=vc, cwd=cwd)
        except NotImplementedError as e:  # pragma: no cover
            print(e)
            sys.exit(1)
        except CalledProcessError as c:  # pragma: no cover
            # cut off usage and exit
            output = c.output.splitlines()[0]
            print(output)
            sys.exit(c.returncode)
        r.fix()

    except KeyboardInterrupt:  # pragma: no cover
        return 1


def create_parser():
    """Create the parser for the pep8radius CLI."""
    description = ("PEP8 clean only the parts of the files which you have "
                   "touched since the last commit, previous commit or "
                   "branch.")
    epilog = ("Run before you commit, against a previous commit or "
              "branch before merging.")
    parser = ArgumentParser(description=description,
                            epilog=epilog,
                            prog='pep8radius')

    parser.add_argument('rev',
                        help='commit or name of branch to compare against',
                        nargs='?')
    parser.add_argument('--version',
                        help='print version number and exit',
                        action='store_true')

    parser.add_argument('--config',
                        default='',
                        help='path to pep8 config file; '
                        "don't pass anything and global and local "
                        'config files will be used; pass False or '
                        'a non-existent file to use defaults')
    parser.add_argument('-d', '--diff', action='store_true', dest='diff',
                        help='print the diff of fixed source vs original')
    parser.add_argument('-i', '--in-place', action='store_true',
                        help="make the fixes in place; modify the files")

    parser.add_argument('--no-color', action='store_true',
                        help='do not print diffs in color '
                             '(default is to use color)')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose',
                        default=0,
                        help='print verbose messages; '
                        'multiple -v result in more verbose messages '
                        '(one less -v is passed to autopep8)')

    ap = parser.add_argument_group('pep8', 'Pep8 options to pass to autopep8.')
    ap.add_argument('-p', '--pep8-passes', metavar='n',
                    default=-1, type=int,
                    help='maximum number of additional pep8 passes '
                    '(default: infinite)')
    ap.add_argument('-a', '--aggressive', action='count', default=0,
                    help='enable non-whitespace changes; '
                    'multiple -a result in more aggressive changes')
    ap.add_argument('--experimental', action='store_true',
                    help='enable experimental fixes')
    ap.add_argument('--exclude', metavar='globs',
                    help='exclude file/directory names that match these '
                    'comma-separated globs')
    ap.add_argument('--list-fixes', action='store_true',
                    help='list codes for fixes and exit; '
                    'used by --ignore and --select')
    ap.add_argument('--ignore', metavar='errors', default='',
                    help='do not fix these errors/warnings '
                    '(default: {0})'.format(DEFAULT_IGNORE))
    ap.add_argument('--select', metavar='errors', default='',
                    help='fix only these errors/warnings (e.g. E4,W)')
    ap.add_argument('--max-line-length', metavar='n', default=79, type=int,
                    help='set maximum allowed line length '
                    '(default: %(default)s)')
    ap.add_argument('--indent-size', default=DEFAULT_INDENT_SIZE,
                    type=int, metavar='n',
                    help='number of spaces per indent level '
                    '(default %(default)s)')

    df = parser.add_argument_group('docformatter',
                                   'Fix docstrings for PEP257.')
    df.add_argument('-f', '--docformatter', action='store_true',
                    help='Use docformatter')
    df.add_argument('--no-blank', dest='post_description_blank',
                    action='store_false',
                    help='Do not add blank line after description')
    df.add_argument('--pre-summary-newline',
                    action='store_true',
                    help='add a newline before the summary of a '
                    'multi-line docstring')
    df.add_argument('--force-wrap', action='store_true',
                    help='force descriptions to be wrapped even if it may '
                    'result in a mess')

    return parser


def parse_args(arguments=None, root=None, apply_config=False):
    """Parse the arguments from the CLI.

    If apply_config then we first look up and apply configs using
    apply_config_defaults.

    """
    if arguments is None:
        arguments = []

    parser = create_parser()
    if apply_config:
        apply_config_defaults(parser, arguments, root=root)
    args = parser.parse_args(arguments)

    # sanity check args (from autopep8)
    if args.max_line_length <= 0:  # pragma: no cover
        parser.error('--max-line-length must be greater than 0')

    if args.select:
        args.select = _split_comma_separated(args.select)

    if args.ignore:
        args.ignore = _split_comma_separated(args.ignore)
    elif not args.select and args.aggressive:
        # Enable everything by default if aggressive.
        args.select = ['E', 'W']
    else:
        args.ignore = _split_comma_separated(DEFAULT_IGNORE)

    if args.exclude:
        args.exclude = _split_comma_separated(args.exclude)
    else:
        args.exclude = []

    return args


def apply_config_defaults(parser, arguments, root):
    """Update the parser's defaults from either the arguments' config_arg or
    the config files given in config_files(root)."""
    if root is None:
        from pep8radius.vcs import VersionControl
        root = VersionControl.which().root_dir()

    config_file = config_arg(arguments)

    config = SafeConfigParser()
    config.read(config_file or config_files(root))
    try:
        defaults = dict((k.replace('-', '_'), v)
                        for k, v in config.items("pep8"))
        parser.set_defaults(**defaults)
    except NoSectionError:
        pass  # just do nothing, potentially this could raise ?
    return parser


def config_arg(arguments):
    """Get --config arg from arguments.
    """
    for arg in arguments:
        if arg.startswith('--config'):
            config_file = arg[9:]
            return os.path.expanduser(config_file)


def config_files(root, home='~'):
    """Returns a list of the global config files and local config files
    found in the root directory.

    Note as we pass this into config.read, where later config files are
    considered more important than preceding. That is later files override
    the settings of previous files.

    """
    home = os.path.expanduser('~')
    local_configs = [os.path.join(root, c) for c in PROJECT_CONFIG]
    global_configs = [DEFAULT_CONFIG] + [os.path.join(home, c)
                                         for c in PROJECT_CONFIG]
    return global_configs + local_configs


def _split_comma_separated(string):
    """Return a set of strings."""
    return set(filter(None, string.split(',')))


def _main(args=None, vc=None, cwd=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    return main(args=args, vc=vc, cwd=cwd, apply_config=True)


if __name__ == "__main__":  # pragma: no cover
    _main()

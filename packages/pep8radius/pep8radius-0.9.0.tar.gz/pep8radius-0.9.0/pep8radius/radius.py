"""This module defines the Radius class, which is where the "meat" of the
pep8radius machinery is done. The important methods are fix, fix_file and
fix_line_range.

The vc attribute is a subclass of VersionControl defined in the vcs
module (provides helper methods for the different vcs e.g. git).

"""

from __future__ import print_function

from sys import version_info

from pep8radius.diff import get_diff, udiff_lines_fixed, print_diff
from pep8radius.vcs import VersionControl


if version_info[0] > 2:  # py3, pragma: no cover
    basestring = str


class Radius(object):

    """PEP8 clean only the parts of the files touched since the last commit, a
    previous commit or branch."""

    def __init__(self, rev=None, options=None, vc=None, cwd=None):
        if vc is None:
            vc = VersionControl.which()
        elif isinstance(vc, basestring):
            vc = VersionControl.from_string(vc)
        else:
            assert(issubclass(vc, VersionControl))
        self.vc = vc(cwd=cwd)

        # pep8radius specific options
        self.rev = self.vc.branch_point(rev)
        from pep8radius.main import parse_args
        self.options = options if options else parse_args([''])
        self.verbose = self.options.verbose
        self.in_place = self.options.in_place
        self.diff = self.options.diff
        self.color = not self.options.no_color

        # autopep8 specific options
        self.options.verbose = max(0, self.options.verbose - 1)
        self.options.in_place = False
        self.options.diff = False

        # Note: This may raise a CalledProcessError, if it does it means
        # that there's been an error with the version control command.
        self.filenames_diff = self.vc.get_filenames_diff(self)

    def fix(self):
        """Runs fix_file on each modified file.

        - Prints progress and diff depending on options.

        """
        n = len(self.filenames_diff)

        self.p('Applying autopep8 to touched lines in %s file(s).' % n)

        total_lines_changed = 0
        pep8_diffs = []
        for i, file_name in enumerate(self.filenames_diff, start=1):
            self.p('%s/%s: %s: ' % (i, n, file_name), end='')
            self.p('', min_=2)

            p_diff = self.fix_file(file_name)
            lines_changed = udiff_lines_fixed(p_diff) if p_diff else 0
            total_lines_changed += lines_changed

            if p_diff and self.diff:
                pep8_diffs.append(p_diff)

        if self.in_place:
            self.p('pep8radius fixed %s lines in %s files.'
                   % (total_lines_changed, n))
        else:
            self.p('pep8radius would fix %s lines in %s files.'
                   % (total_lines_changed, n))

        if self.diff:
            for diff in pep8_diffs:
                print_diff(diff, color=self.color)

    def fix_file(self, file_name):
        """Apply autopep8 to the diff lines of a file.

        - Returns the diff between original and fixed file.
        - If self.in_place then this writes the the fixed code the file_name.
        - Prints dots to show progress depending on options.

        """
        import codecs
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                original = f.read()
        except IOError:
            # file has been removed
            return ''

        # We hope that a CalledProcessError would have already raised
        # during the init if it were going to raise here.
        modified_lines_descending = self.vc.modified_lines(self, file_name)

        # Apply line fixes "up" the file (i.e. in reverse) so that
        # fixes do not affect changes we're yet to make.
        partial = original
        for start, end in modified_lines_descending:
            partial = self.fix_line_range(partial, start, end)
            self.p('.', end='', max_=1)
        self.p('', max_=1)
        fixed = partial

        if self.in_place:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                f.write(fixed)
        return get_diff(original, fixed, file_name)

    def fix_line_range(self, f, start, end):
        """Apply autopep8 between start and end of file f."""
        # not sure on behaviour if outside range (indexing starts at 1)
        start = max(start, 1)

        self.options.line_range = [start, end]
        from autopep8 import fix_code
        fixed = fix_code(f,   self.options)

        if self.options.docformatter:
            from docformatter import format_code
            fixed = format_code(
                fixed,
                summary_wrap_length=self.options.max_line_length - 1,
                description_wrap_length=(self.options.max_line_length
                                         - 2 * self.options.indent_size),
                pre_summary_newline=self.options.pre_summary_newline,
                post_description_blank=self.options.post_description_blank,
                force_wrap=self.options.force_wrap,
                line_range=[start, end])

        return fixed

    def p(self, something_to_print, end=None, min_=1, max_=99):
        """Print if self.verbose is within min_ and max_."""
        if min_ <= self.verbose <= max_:
            import sys
            print(something_to_print, end=end)
            sys.stdout.flush()

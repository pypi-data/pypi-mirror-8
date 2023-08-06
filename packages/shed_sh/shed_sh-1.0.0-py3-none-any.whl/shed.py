#!/usr/bin/env python3

"""
shed v1.0.0

Don't run "curl | sh" again.
Use "curl | shed" to verify scripts before running.

More info: http://github.com/mplewis/shed
"""

import sys
import shlex
import subprocess
import os
from shutil import which
from tempfile import NamedTemporaryFile


def default_editor():
    """
    The user's preferred editor. Tries the env vars $SHED_EDITOR and $EDITOR.
    If those variables aren't set, tries nano, vim, vi, and emacs.
    """
    EDITOR_VARIBLES = ('SHED_EDITOR', 'EDITOR')
    FALLBACK_EDITORS = ('nano', 'vim', 'vi', 'emacs')

    for var in EDITOR_VARIBLES:
        try:
            return os.environ[var]
        except KeyError:
            pass

    for editor in FALLBACK_EDITORS:
        if which(editor):
            return editor

    raise ValueError('Failed to find $SHED_EDITOR, $EDITOR, '
                     'nano, vim, vi, or emacs')


def open_editor(filename):
    """Opens the given file in the user's default editor."""
    try:
        editor = default_editor()
    except ValueError:
        print()
        print("Couldn't find a valid editor in $SHED_EDITOR or $EDITOR. "
              "Try setting one:")
        print('    export SHED_EDITOR=/path/to/my/editor')
        sys.exit(-1)
    editor_split = shlex.split(editor)
    if len(editor_split) > 1:
        editor_split.append(filename)
        subprocess.check_call(editor_split)
    else:
        subprocess.check_call([editor, filename])


def confirm_exec(filename):
    """
    Confirm the user still wants to execute the script.
    Returns True for yes, False for no. No response defaults to yes.
    """

    yes = ('yes', 'y')
    no = ('no', 'n')

    print()  # Pretty print spacing
    raw_resp = input('Do you still want to execute this script? [Y/n]: ')

    while True:
        resp = raw_resp.strip().lower()
        if resp in yes:
            return True
        if resp in no:
            return False
        if not resp:
            return True

        raw_resp = input('Please respond with "yes" or "no" [Y/n]: ')


def main():
    # Print a helpful message if this looks like a user ran it standalone
    my_name = os.path.basename(sys.argv[0])
    if sys.stdin.isatty():
        print('Usage: curl -L https://example.com/some_script.sh | {}'
              .format(my_name))
        return

    # Figure out if we're running as "shed" (sh) or "bashed" (bash).
    # Use sh as the default shell.
    if my_name == 'bashed':
        shell = 'bash'
    else:
        shell = 'sh'

    # Save arguments to be added to sh later.
    # These change later in the script, so be careful!
    extra_args = sys.argv[1:]

    # Get script from pipe
    script = sys.stdin.read()
    # After we consume stdin, we need to reopen it for interactive input
    tty = open('/dev/tty')
    os.dup2(tty.fileno(), 0)

    # Create a temp file to hold our piped script
    with NamedTemporaryFile() as f:
        f.write(script.encode('utf-8'))
        f.flush()
        open_editor(f.name)

        # Ask user for permission to execute modified script
        if confirm_exec(f.name):
            print()  # Pretty print spacing
            # Call selected shell with any extra args passed to shed
            args = [shell]
            args.extend(extra_args)
            args.append(f.name)
            subprocess.call(args)


if __name__ == '__main__':
    main()

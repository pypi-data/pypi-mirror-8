"""This is an automatically generated file created by stsci.distutils.hooks.version_setup_hook.
Do not modify this file by hand.
"""

__all__ = ['__version__', '__vdate__', '__svn_revision__', '__svn_full_info__',
           '__setup_datetime__']

import datetime

__version__ = '0.9.6'
__vdate__ = 'unspecified'
__svn_revision__ = '4309:4312'
__svn_full_info__ = 'Path: pysynphot\nURL: https://aeon.stsci.edu/ssb/svn/astrolib/tags/release_0.9.6\nRepository Root: https://aeon.stsci.edu/ssb/svn/astrolib\nRepository UUID: 90a0a646-be8a-0410-bb88-9290da87bc01\nRevision: 4309\nNode Kind: directory\nSchedule: normal\nLast Changed Author: cslocum\nLast Changed Rev: 4308\nLast Changed Date: 2014-10-08 15:33:07 -0400 (Wed, 08 Oct 2014)'
__setup_datetime__ = datetime.datetime(2014, 10, 8, 17, 4, 40, 457366)

# what version of stsci.distutils created this version.py
stsci_distutils_version = '0.3.8.dev34759'

if '.dev' in __version__:
    def update_svn_info():
        """Update the SVN info if running out of an SVN working copy."""

        import os
        import string
        import subprocess

        global __svn_revision__
        global __svn_full_info__

        path = os.path.abspath(os.path.dirname(__file__))

        run_svnversion = True

        try:
            pipe = subprocess.Popen(['svn', 'info', path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            stdout, _ = pipe.communicate()
            if pipe.returncode == 0:
                lines = []
                for line in stdout.splitlines():
                    line = line.decode('latin1').strip()
                    if not line:
                        continue
                    lines.append(line)

                if not lines:
                    __svn_full_info__ = ['unknown']
                else:
                    __svn_full_info__ = lines
            else:
                run_svnversion = False
        except OSError:
            run_svnversion = False

        if run_svnversion:
            # If updating the __svn_full_info__ succeeded then use its output
            # to find the base of the working copy and use svnversion to get
            # the svn revision.
            for line in __svn_full_info__:
                if line.startswith('Working Copy Root Path'):
                    path = line.split(':', 1)[1].strip()
                    break

            try:
                pipe = subprocess.Popen(['svnversion', path],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                stdout, _ = pipe.communicate()
                if pipe.returncode == 0:
                    stdout = stdout.decode('latin1').strip()
                    if stdout and stdout[0] in string.digits:
                        __svn_revision__ = stdout
            except OSError:
                pass

        # Convert __svn_full_info__ back to a string
        if isinstance(__svn_full_info__, list):
            __svn_full_info__ = '\n'.join(__svn_full_info__)


    update_svn_info()
    del update_svn_info

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------


from distutils.core import setup, Command
import sys
import subprocess

# Uncomment this to package with setuptools. Then extras_require is usable
#try:
#    import setuptools
#except ImportError:
#    pass


class PyTest(Command):
    """Class for running py.test via setup.py"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='pyspread',
    version='0.4',
    description='Python spreadsheet',
    long_description='Pyspread is a non-traditional spreadsheet application'
    ' that is based on and written in the programming language Python.',
    license='GPL v3 :: GNU General Public License',
    keywords=['spreadsheet', 'pyspread'],
    author='Martin Manns',
    author_email='mmanns@gmx.net',
    url='http://manns.github.io/pyspread/',
    requires=['numpy (>=1.1)', 'wx (>=2.8.10)', 'matplotlib (>=1.1.1)',
              'pycairo (>=1.8.8)'],
#    extras_require = {
#        'GPG': ['gnupg>=0.3.0'],
#        'SVG': [],  # May require python_rsvg if not shipped with pyCairo
#        'XLS': ['xlrd>=0.9.1', 'xlwt>=0.7.5'],
#        'code_completion': ['jedi>=0.8'],
#        'basemap': ['basemap>=1.0.7'],
#    },
    packages=['pyspread'],
    scripts=['pyspread/pyspread'],
    cmdclass={'test': PyTest},
    package_data={'pyspread': [
            '*.py',
            '../pyspread.sh',
            '../pyspread.bat',
            '../runtests.py',
            'src/*.py',
            'src/pyspread',
            'src/*/*.py',
            'src/*/test/*.py',
            'src/*/test/*.pys*',
            'src/*/test/*.sig',
            'src/*/test/*.csv',
            'src/*/test/*.xls',
            'src/*/test/*.txt',
            'src/*/test/*.svg',
            'src/*/test/*.pys*',
            'share/icons/*.png',
            'share/icons/*.ico',
            'share/icons/Tango/24x24/actions/*.png',
            'share/icons/Tango/24x24/toggles/*.png',
            'share/icons/Tango/24x24/toggles/*.xpm',
            'share/icons/Tango/24x24/status/*.png',
            'doc/help/*.html',
            'doc/help/images/*.png',
            'po/*',
            'locale/*/*/*.mo',
            'examples/*',
            'COPYING',
            'thanks',
            'faq',
            '*.1',
            'authors',
            '../pyspread.pth',
            '../README',
            '../changelog'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)

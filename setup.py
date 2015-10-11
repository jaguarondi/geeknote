#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import getpass
import codecs
import geeknote
from setuptools import setup
from setuptools.command.install import install


BASH_COMPLETION = '''
_geeknote_command()
{
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    SAVE_IFS=$IFS
    IFS=" "
    args="${COMP_WORDS[*]:1}"
    IFS=$SAVE_IFS

    COMPREPLY=( $(compgen -W "`geeknote autocomplete ${args}`" -- ${cur}) )

    return 0
}
complete -F _geeknote_command geeknote
'''


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


class full_install(install):

    user_options = install.user_options + [
        ('userhome=', None,
         "(Linux only) Set user home directory for"
         " bash completion ({0})"
         .format(os.path.expanduser('~')))
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.userhome = ''

    def run(self):
        if sys.platform == 'linux2':
            self.install_autocomplite()
        install.run(self)

    def install_autocomplite(self):
        if self.userhome:
            self.userhome = '{0}/.bash_completion'.format(self.userhome)
        else:
            self.userhome = '{0}/.bash_completion'.format(os.path.expanduser('~'))

        if not os.path.exists(self.userhome) or \
           BASH_COMPLETION not in open(self.userhome, 'r').read():
            with open(self.userhome, 'a') as completion:
                print('Autocomplete was written to {0}'.format(self.userhome))
                completion.write(BASH_COMPLETION)


setup(
    name='geeknote',
    version=geeknote.__version__,
    license='GPL',
    author='Vitaliy Rodnenko',
    author_email='vitaliy@rodnenko.ru',
    description='Geeknote - is a command line client for Evernote, '
                'that can be use on Linux, FreeBSD and OS X.',
    long_description=read("README.md"),
    url='http://www.geeknote.me',
    packages=['geeknote'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

    install_requires=[
        'evernote>=1.17',
        'html2text',
        'sqlalchemy',
        'markdown2',
        'beautifulsoup4',
        'thrift'
    ],

    entry_points={
        'console_scripts': [
            'geeknote = geeknote.geeknote:main',
            'gnsync = geeknote.gnsync:main'
        ]
    },
    cmdclass={
        'install': full_install
    },
    platforms='Any',
    test_suite='tests',
    zip_safe=False,
    keywords='Evernote, console'
)

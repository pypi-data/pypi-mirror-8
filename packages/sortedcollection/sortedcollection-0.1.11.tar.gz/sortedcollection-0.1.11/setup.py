#!/usr/bin/env python

import os
import sys
import fnmatch

## prepare to run PyTest as a command
from distutils.core import Command

## explain this...
#from distribute_setup import use_setuptools
#use_setuptools()

from setuptools import setup, find_packages

from version import get_git_version
PROJECT = 'sortedcollection'
VERSION, SOURCE_HASH = get_git_version()
AUTHOR = 'Diffeo, Inc.'
AUTHOR_EMAIL = 'support@diffeo.com'
DESC = 'SortedCollection class that abstracts bisect extended from http://code.activestate.com/recipes/577197-sortedcollection/.'

def read_file(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
        )
    return open(file_path).read()

def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
      goodfiles = fnmatch.filter(files, pattern)
      results.extend(os.path.join(base, f) for f in goodfiles)
    return results

class PyTest(Command):
    '''run py.test'''

    description = 'runs py.test to execute all tests'

    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    #long_description=read_file('README.md'),
    long_description="",
    license='MIT/X11 license http://opensource.org/licenses/MIT',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url='',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    cmdclass = {'test': PyTest},
    # We can select proper classifiers later
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',  ## MIT/X11 license http://opensource.org/licenses/MIT
    ],
    install_requires=[
        'pytest',
    ],
    # include_package_data = True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any files found in the 'data' package:
        # '': recursive_glob('src/data/', '*')
        '': recursive_glob('data/', '*')
    }
)

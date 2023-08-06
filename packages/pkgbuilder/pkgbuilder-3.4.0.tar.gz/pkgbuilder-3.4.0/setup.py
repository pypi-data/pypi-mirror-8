#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import codecs
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests.py']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='pkgbuilder',
      version='3.4.0',
      description='An AUR helper (and library) in Python 3.',
      keywords='arch pkgbuild',
      author='Chris Warrick',
      author_email='chris@chriswarrick.com',
      url='https://github.com/Kwpolska/pkgbuilder',
      license='3-clause BSD',
      long_description=codecs.open('./docs/README.rst', 'r', 'utf-8').read(),
      platforms='Arch Linux',
      zip_safe=False,
      cmdclass={'test': PyTest},
      classifiers=['Development Status :: 6 - Mature',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: System',
                   'Topic :: System :: Archiving :: Packaging',
                   'Topic :: Utilities'],
      packages=['pkgbuilder'],
      requires=['pyalpm', 'requests'],
      data_files=[('share/man/man8', ['docs/pkgbuilder.8.gz']),
                  ('share/man/man8', ['docs/pb.8.gz']),
                  ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/'
                                                   'pkgbuilder.mo']),
                  ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/'
                                                   'pkgbuilder.mo'])],
      entry_points={
          'console_scripts': [
              'pkgbuilder = pkgbuilder.__main__:pkgbuildermain',
              'pb = pkgbuilder.__main__:pbwrappermain'
          ]
      },
      )

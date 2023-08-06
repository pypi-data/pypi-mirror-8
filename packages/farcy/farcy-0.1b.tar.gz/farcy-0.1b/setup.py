"""Farcy setup.py."""

import os
import re
from setuptools import setup

PACKAGE_NAME = 'farcy'

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst')) as fp:
    README = fp.read()
with open(os.path.join(HERE, PACKAGE_NAME, '__init__.py')) as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)


setup(name=PACKAGE_NAME,
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4'],
      description='A code review bot for github pull requests',
      entry_points={'console_scripts':
                    ['{0} = {0}:main'.format(PACKAGE_NAME)]},
      extras_require={'python': ['flake8 >= 2.2.5', 'pep257 >= 0.3.2']},
      install_requires=['botocore >= 0.74.0',
                        'docopt >= 0.6.2',
                        'github3.py >= 0.9.3',
                        'update_checker >= 0.11'],
      keywords=['code review', 'pull request'],
      license='Simplified BSD License',
      long_description=README,
      packages=[PACKAGE_NAME],
      test_suite='test',
      url='https://github.com/appfolio/farcy',
      version=VERSION)

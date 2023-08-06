from setuptools import setup

from sys import version

if version < '2.6.0':
    raise Exception("This module doesn't support any version less than 2.6")

import sys

sys.path.append("./test")

with open('README.rst', 'r') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    "Programming Language :: Python",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

requires = ['selenium>=2.44.0']
tests_requires = ['mock', 'nose']

if version < '2.7.0':
    tests_requires.append('unittest2')

setup(
    author='Keita Oouchi',
    author_email='keita.oouchi@gmail.com',
    url='https://github.com/keitaoouchi/seleniumwrapper',
    name='seleniumwrapper',
    version='0.5.4',
    package_dir={"": "src"},
    packages=['seleniumwrapper'],
    license='BSD License',
    classifiers=classifiers,
    description='selenium webdriver wrapper to make manipulation easier.',
    long_description=long_description,
    install_requires=requires,
    tests_require=tests_requires,
    test_suite='test'
)

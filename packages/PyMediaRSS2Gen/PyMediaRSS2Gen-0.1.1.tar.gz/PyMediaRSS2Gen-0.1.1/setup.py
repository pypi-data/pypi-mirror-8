# coding=utf-8
"""Setup script to install PyMediaRSS2Gen."""

import sys
from setuptools import setup

install_requires = ['PyRSS2Gen']
if sys.version_info < (2, 7):
    install_requires.append('ordereddict')

try:
    long_description = \
        open('README.rst').read() + '\n\n' + \
        open('CHANGELOG.rst').read() + '\n\n' + \
        open('AUTHORS.rst').read()
except (OSError, IOError):
    long_description = ''

setup(
    name='PyMediaRSS2Gen',
    version='0.1.1',
    description='A Python library for generating Media RSS 2.0 feeds.',
    long_description=long_description,
    author='Dirk Weise',
    author_email='code@dirk-weise.de',
    license='MIT',
    url='https://github.com/wedi/PyMediaRSS2Gen',
    download_url='https://github.com/wedi/PyMediaRSS2Gen/archive/v0.1.1.tar.gz',  # noqa
    keywords=['RSS', 'Feed'],
    install_requires=install_requires,
    py_modules=['PyMediaRSS2Gen'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
    ],
)

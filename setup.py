#!/usr/bin/python3

import sys
import os
from setuptools import setup


if sys.version_info[0] != 3:
    sys.exit("Python3 is required in order to install hexsticker")


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


def get_version():
    with open(os.path.join('hexsticker', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


def get_long_description():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='hexsticker',
    version=get_version(),
    entry_points={
        'console_scripts': ['hexsticker=hexsticker.cli:hexsticker']
    },
    packages=['hexsticker'],
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fridolin.pokorny@gmail.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin.pokorny@gmail.com',
    description='Convert any image to image that conforms with hexagon stickers standard.',
    long_description=get_long_description(),
    url='https://github.com/fridex/hexsticker',
    license='GPLv2',
    keywords='hexagon stickers hexagon-stickers',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Utilities"
    ]
)

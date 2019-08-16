#!/usr/bin/env python

import setuptools
from distutils.core import setup

if __name__ == '__main__':
    setup(
        name="treedistancegenerator",
        version="0.1",
        descriptions="Generate randomised trees",
        author="Eileen Kuehn",
        author_email="eileen.kuehn@kit.edu",
        url="https://github.com/eileen-kuehn/treedistancegenerator",
        packages=setuptools.find_packages(),
        dependency_links=[],
        install_requires=[],
        # unit tests
        test_suite='treedistancegenerator_tests',
    )

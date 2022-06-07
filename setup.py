#
# file setup.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

import io
from setuptools import setup, find_packages

setup(
    name='simpleadb',
    version='0.3.2',
    description='Python wrapper for adb protocol.',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    author='Michal Kielan',
    author_email='michalkielan@protonmail.com',
    url='https://github.com/michalkielan/simple-adb',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>3.0.0',
    test_suite='tests',
)

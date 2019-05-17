from setuptools import setup, find_packages
import sys

setup(
  name='simpleadb',
  version='0.1.0',
  description='Python wrapper for adb protocol',
  author='Michal Kielan',
  author_email='michalkielan@protonmail.com',
  url='https://github.com/michalkielan/simple-adb',
  packages=find_packages(exclude=('tests', 'docs')),
  python_requires='>3.0.0',
  test_suite='tests',
)

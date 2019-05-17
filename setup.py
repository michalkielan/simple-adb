from setuptools import setup, find_packages
import sys

if sys.version_info < (3,0):
  print('Error, python < 3.0 is not supported')

#with open('README.md') as f:
#  readme = f.read()
#
#with open('LICENSE') as f:
#  license = f.read()

setup(
  name='simpleadb',
  version='0.1.0',
  description='Python wrapper for adb protocol',
#  long_description=readme,
  author='Michal Kielan',
  author_email='michalkielan@protonmail.com',
  url='https://github.com/michalkielan/simple-adb',
#  license=license,
  packages=find_packages(exclude=('tests', 'docs')),
  python_requires='>3.4.0',
  test_suite='tests',
)

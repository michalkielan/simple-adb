from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name='simpleadb',
  version='0.1.0',
  description='Python wrapper for adb protocol',
  long_description=readme,
  author='Michal Kielan',
  author_email='michalkielan@protonmail.com',
  url='https://github.com/michalkielan/simple-adb',
  license=license,
  packages=find_packages(exclude=('tests', 'docs')),
  test_suite='tests',
)

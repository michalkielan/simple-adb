from setuptools import setup

setup(
   name='simpleadb',
   version='0.0.1',
   description='Adb wrapper',
   author='Micha Kielan',
   author_email='michalkielan@protonmail.com',
   packages=['simpleadb'],
   package_dir={'simpleadb':'simpleadb'},
   test_suite="tests"
)

#!/bin/sh
wget $APK_URL
python setup.py install
tox

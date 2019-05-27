#!/bin/bash
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
android list target
echo no | android create avd --force -n test -t $ANDROID_API --abi armeabi-v7a -c 100M
emulator -avd test -no-skin -no-window &
android-wait-for-emulator
adb shell input keyevent 82 &

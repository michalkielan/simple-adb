#
# file utils.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Utils for tests"""
import os
import shutil
import time
import wget

DUMMY_APK_VERSION = '0.0.1'
DUMMY_APK_NAME = 'app-debug.apk'
DUMMY_APK_URL = (
    f'https://github.com/michalkielan/AndroidDummyApp/releases/download/{DUMMY_APK_VERSION}/{DUMMY_APK_NAME}')
DUMMY_PACKAGE_NAME = 'com.dummy_app.dummy'


def get_test_device_id():
    """Get test device serial number"""
    return os.environ['TEST_DEVICE_ID']


def get_adb_path():
    """Get adb binary path"""
    return shutil.which('adb')


def is_github_workflows_env():
    """Return True if github workflows environment"""
    return os.environ.get('ENVIRONMENT', '') == 'GITHUB_WORKFLOWS'


def android_wait_for_emulator():
    """Wait for android emulator"""
    if is_github_workflows_env():
        os.system(
            "adb wait-for-device shell \'while [[ -z $(getprop \
            sys.boot_completed)]]; do sleep 1; done; input keyevent 82\'"
        )


def download_resources():
    """Download resources for tests"""
    if not os.path.exists(DUMMY_APK_NAME):
        wget.download(DUMMY_APK_URL, DUMMY_APK_NAME)
    while not os.path.exists(DUMMY_APK_NAME):
        time.sleep(1)

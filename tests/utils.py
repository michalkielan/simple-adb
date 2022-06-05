#
# file utils.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Utils for tests"""
import os


def get_test_device_id():
    """Get test device serial number"""
    return os.environ['TEST_DEVICE_ID']


def get_adb_path():
    """Get adb binary path"""
    return '/usr/local/android-sdk/platform-tools/adb'


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

#
# file test_adb_server.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb commands"""
import os
import unittest
import simpleadb


def get_test_device_id():
    """Get test device serial number"""
    return os.environ['TEST_DEVICE_ID']


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


TEST_DEVICE_ID = get_test_device_id()


class AdbServerTest(unittest.TestCase):
    """Adb server unit tests"""

    def setUp(self):
        """Setup test"""

    def tearDown(self):
        """Teardown test"""

    def test_adb_devices(self):
        """Check if adb server is running correctly"""
        adb = simpleadb.AdbServer()
        android_wait_for_emulator()
        devices = adb.devices()
        if not devices:
            self.fail('No adb devices found')
        emulator = devices[0]
        self.assertTrue(TEST_DEVICE_ID in emulator.get_id())

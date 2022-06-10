#
# file test_adb_server.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb commands"""
import unittest
import simpleadb
from .utils import android_wait_for_emulator, get_test_device_id


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
            self.fail("No adb devices found")
        device_exists = False
        for device in devices:
            if get_test_device_id() == device.get_id():
                device_exists = True
        self.assertTrue(device_exists)

"""Unit tests for adb commands"""
import os
import unittest
import simpleadb


def get_test_device_id():
    """Get test device serial number"""
    return os.environ['TEST_DEVICE_ID']


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
        devices = adb.devices()
        if not devices:
            self.fail('No adb devices found')
        emulator = devices[0]
        self.assertTrue(TEST_DEVICE_ID in emulator.get_id())

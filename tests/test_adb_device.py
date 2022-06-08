#
# file test_adb_device.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb commands"""
import unittest
import os
import subprocess
import pytest
import simpleadb
from . import utils

TEST_DEVICE_ID = utils.get_test_device_id()


class AdbDeviceTest(  # pylint: disable=too-many-public-methods
        unittest.TestCase):
    """Adb device unit tests"""

    @classmethod
    def setUpClass(cls):
        """Download resources at the beginning of the tests"""
        utils.download_resources()

    def setUp(self):
        """Start adb server in each test"""
        self.__adb = simpleadb.AdbServer()
        utils.android_wait_for_emulator()

    def tearDown(self):
        """Kill adb server in each test"""
        self.__adb.kill()

    def test_devices_exists(self):
        """Check if adb devices exists"""
        devices = self.__adb.devices()
        if not devices:
            self.fail('No adb devices found')
        test_device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertTrue(test_device in devices)

    def test_device_eq_to_device_string(self):
        """Test equal operator for adb device object"""
        dev1 = simpleadb.AdbDevice('1234')
        dev2 = simpleadb.AdbDevice('1234')
        dev3 = simpleadb.AdbDevice('42')
        self.assertEqual(dev1, dev2)
        self.assertNotEqual(dev1, dev3)

    def test_str(self):
        """Test qual operator for adb device and object and string devie id"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertEqual(TEST_DEVICE_ID, str(device))

    def test_custom_adb_path(self):
        """Test custom adb binary path"""
        device = simpleadb.AdbDevice(
            TEST_DEVICE_ID,
            path=utils.get_adb_path()
        )
        self.assertTrue(device.is_available())

    def test_custom_adb_path_no_exists(self):
        """Test custom adb binary path not exists"""
        device = simpleadb.AdbDevice(
            TEST_DEVICE_ID,
            path='dummy/path'
        )
        with self.assertRaises(subprocess.CalledProcessError):
            device.get_serialno()

    @pytest.mark.skipif(
        utils.is_github_workflows_env(),
        reason='is_root() is "experimental" feature, may fail on emulator')
    def test_is_root_true(self):
        """Check if device is rooted after adb root command"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.root(timeout_sec=10)
        self.assertEqual(res, 0)
        self.assertTrue(device.is_root())

    def test_adb_root(self):
        """Check adb root command not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.root()
        self.assertEqual(res, 0)

    def test_get_id(self):
        """Check if get_id is equal to test device id"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        test_device_id = device.get_id()
        self.assertEqual(test_device_id, TEST_DEVICE_ID)

    def test_get_serialno(self):
        """Check if get_serialno is equal to test device id"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        test_device_id = device.get_serialno()
        self.assertEqual(test_device_id, TEST_DEVICE_ID)

    def test_input_tap(self):
        """Check if input tap is not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        res = device.tap(1, 1)
        self.assertEqual(res, 0)

    def test_input_swipe(self):
        """Check if input swipe is not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        res = device.swipe(1, 1, 2, 2)
        self.assertEqual(res, 0)

    def test_screencap(self):
        """Check if screenshot file exists after screencap"""
        filepath = './screenshot.png'
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.screencap(local=filepath)
        device.screencap()
        self.assertEqual(res, 0)
        self.assertTrue(os.path.isfile(filepath))

    def test_install(self):
        """Check if install and uninstall apk are not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        device.remount()
        res = device.install(utils.DUMMY_APK_NAME)
        self.assertEqual(res, 0)
        res = device.uninstall(utils.DUMMY_PACKAGE_NAME)
        self.assertEqual(res, 0)

    def test_setprop(self):
        """Check if setprop is not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        res = device.setprop("dummy_prop", "true")
        self.assertEqual(res, 0)

    def test_getprop(self):
        """Verify if property value is correct using getprop command"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        prop_name = 'dummy_prop'
        prop_val = 'true'
        if not device.is_root():
            device.root()
        res = device.setprop(prop_name, prop_val)
        self.assertEqual(res, 0)
        self.assertEqual(prop_val, device.getprop(prop_name))

    @pytest.mark.skipif(
        utils.is_github_workflows_env(),
        reason='Failing on emulator')
    def test_verity(self):
        """Check if verity command is not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        device.root()
        device.remount()
        res = device.enable_verity(True)
        self.assertEqual(res, 0)
        res = device.enable_verity(False)
        self.assertEqual(res, 0)

    def test_push_pull(self):
        """Verify if file exists after push/pull command"""
        filename = 'dummy_file'
        dest = '/sdcard/'

        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        os.system('touch ' + filename)
        res = device.push(filename, dest)
        self.assertEqual(res, 0)

        os.remove(filename)
        self.assertFalse(os.path.isfile(filename))
        res = device.pull(dest + filename)
        self.assertEqual(res, 0)
        self.assertTrue(os.path.isfile(filename))

    def test_remove(self):
        """Check if file was removed after rm command"""
        filename = 'test_remove_dummy_file'
        dest = '/sdcard/'

        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        os.system('touch ' + filename)
        res = device.push(filename, dest)
        self.assertEqual(res, 0)

        os.remove(filename)
        device.rm(dest + filename)

        with self.assertRaises(subprocess.CalledProcessError):
            res = device.pull(dest + filename)
            self.assertNotEqual(res, 0)

    def test_remove_failure(self):
        """Check if rm command failed if file not exists"""
        filename = '/sdcard/no_existing_file'
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)

        with self.assertRaises(subprocess.CalledProcessError):
            res = device.rm(filename)
            self.assertNotEqual(res, 0)

    def test_get_state(self):
        """Check adb get state command"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        state = device.get_state()
        self.assertEqual(state, 'device')

    def test_dump_logcat(self):
        """Test dump logcat"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        log = device.dump_logcat()
        self.assertNotEqual(log, None)

    def test_dump_logcat_from_buffer(self):
        """Test dump logcat"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        log = device.dump_logcat('main')
        self.assertNotEqual(log, None)

    def test_clear_logcat(self):
        """Test clear logcat"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.clear_logcat()
        self.assertEqual(res, 0)

    def test_clear_logcat_buf(self):
        """Test clear logcat from main buffer"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.clear_logcat('main')
        self.assertEqual(res, 0)

    @pytest.mark.skipif(
        utils.is_github_workflows_env(),
        reason='Failing on emulator')
    def test_device_is_available(self):
        """Test if device is available"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        if not device.is_root():
            device.root()
        self.assertTrue(device.is_available())

    def test_no_available(self):
        """Test if device not available"""
        device = simpleadb.AdbDevice('dummy_id')
        self.assertFalse(device.is_available())

    def test_wait_for_device(self):
        """Test wait for device"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.wait_for_device()
        self.assertEqual(0, res)

    def test_wait_for_device_failed(self):
        """Wait for device failed after timeout if device not exists"""
        with self.assertRaises(subprocess.TimeoutExpired):
            device = simpleadb.AdbDevice('dummy-device')
            device.wait_for_device(timeout=1)

    def test_wait_for_device_timeout(self):
        """Test wait for device with custom timeout"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        device.root()
        res = device.wait_for_device(timeout=5)
        self.assertEqual(0, res)

    def test_adb_shell(self):
        """Test adb shell input command"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        device.root()
        res = device.shell('input text 42')
        self.assertEqual(0, res)

    def test_unroot(self):
        """Test unroot"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        res = device.unroot()
        self.assertEqual(res, 0)

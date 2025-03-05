#
# file test_adb_device.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb commands."""

import unittest
import os
import pytest
from interruptingcow import timeout
import simpleadb
from simpleadb.utils import is_valid_ip
from .utils import (
    DUMMY_APK_NAME,
    DUMMY_PACKAGE_NAME,
    android_wait_for_emulator,
    download_resources,
    enable_root_tests,
    get_adb_path,
    get_test_device_id,
    is_github_workflows_env,
)

TEST_DEVICE_ID = get_test_device_id()


class AdbDeviceTest(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Adb device unit tests."""

    @classmethod
    def setUpClass(cls):
        """Start adb server and download tests resources at the beginning of
        the tests."""
        simpleadb.AdbServer()
        download_resources()

    def setUp(self):
        """Start adb server in each test."""
        android_wait_for_emulator()

    def test_adb_check_command_exception_error(self):
        """Check AdbCommandError exception."""
        device_id = "dummy_device_id"
        output = "dummy_output"
        try:
            raise simpleadb.AdbCommandError(device_id, output, None)
        except simpleadb.AdbCommandError as err:
            self.assertEqual(output, str(err))
            self.assertEqual(device_id, err.device_id)
            self.assertEqual(None, err.called_process_error)

    def test_adb_device_repr_is_same_as_id(self):
        """Check if repr is same as get_id()."""
        test_device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertEqual(repr(test_device), test_device.get_id())

    def test_adb_devices_exists(self):
        """Check if adb devices exists."""
        adb_server = simpleadb.AdbServer()
        devices = adb_server.devices()
        if not devices:
            self.fail("No adb devices found")
        test_device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertTrue(test_device in devices)

    def test_device_eq_to_device_string(self):
        """Test equal operator for adb device object."""
        dev1 = simpleadb.AdbDevice("1234")
        dev2 = simpleadb.AdbDevice("1234")
        dev3 = simpleadb.AdbDevice("42")
        self.assertEqual(dev1, dev2)
        self.assertNotEqual(dev1, dev3)

    def test_adb_device_is_str(self):
        """Test qual operator for adb device and string devie id."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertEqual(TEST_DEVICE_ID, str(device))

    def test_custom_adb_path_not_failing(self):
        """Test custom adb binary path"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID, path=get_adb_path())
        self.assertTrue(device.is_available())

    def test_custom_adb_path_not_exists(self):
        """Test custom adb binary path not exists."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID, path="dummy/path")
        with self.assertRaises(simpleadb.AdbCommandError):
            device.get_serialno()

    @pytest.mark.skipif(
        is_github_workflows_env() or not enable_root_tests(),
        reason='is_root() is "experimental" feature, may fail on emulator',
    )
    def test_is_root_true_when_device_rooted(self):
        """Check if device is rooted after adb root command."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.root(timeout_sec=10)
        except simpleadb.AdbCommandError as err:
            self.fail(err)
        self.assertTrue(device.is_root())

    @pytest.mark.skipif(
        not enable_root_tests(), reason="Failing on not rootable devices"
    )
    def test_adb_root_not_failing(self):
        """Check adb root command not failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.root()
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_get_id_returns_correct_id(self):
        """Check if get_id is equal to test device id."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        test_device_id = device.get_id()
        self.assertEqual(test_device_id, TEST_DEVICE_ID)

    def test_get_serialno_returns_correct_id(self):
        """Check if get_serialno is equal to test device id."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        test_device_id = device.get_serialno()
        self.assertEqual(test_device_id, TEST_DEVICE_ID)

    def test_input_tap_not_failing(self):
        """Check if input tap is not failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.tap(1, 1)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_input_swipe_not_failing(self):
        """Check if input swipe is not failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.swipe(1, 1, 2, 2)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_screenshot_if_screenshot_file_exists(self):
        """Check if screenshot file exists after screencap."""
        filepath = "./screenshot.png"
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.screencap(local=filepath)
            device.screencap()
        except simpleadb.AdbCommandError as err:
            self.fail(err)
        self.assertTrue(os.path.isfile(filepath))

    def test_get_pid_of_running_app(self):
        """Get PID of running app."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        package = DUMMY_PACKAGE_NAME
        try:
            device.install(DUMMY_APK_NAME)
            device.shell(f"am start -n {package}/{package}.MainActivity")
        except simpleadb.AdbCommandError as err:
            self.fail(err)
        wait_for_start_app_sec = 10
        try:
            with timeout(wait_for_start_app_sec, exception=RuntimeError):
                while True:
                    try:
                        pid = device.get_app_pid(package)
                        self.assertTrue(isinstance(pid, int))
                        self.assertTrue(pid != 0)
                        break
                    except simpleadb.AdbCommandError:
                        pass
        except RuntimeError as err:
            self.fail(err)
        try:
            device.uninstall(package)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_install_non_exist_apk_failed(self):
        """Check if install is failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        with self.assertRaises(simpleadb.AdbCommandError):
            device.install("apk_not_exists")

    def test_uninstall_non_exist_apk_failed(self):
        """Check if uninstall apk is failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        with self.assertRaises(simpleadb.AdbCommandError):
            device.uninstall("apk_not_exists")

    @pytest.mark.skipif(
        not enable_root_tests(), reason="Failing on not rootable devices"
    )
    def test_set_setprop_is_not_failing(self):
        """Check if setprop is not failing"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.setprop("dummy_prop", "true")
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    @pytest.mark.skipif(
        not enable_root_tests(), reason="Failing on not rootable devices"
    )
    def test_getprop(self):
        """Verify if property value is correct using getprop command."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        prop_name = "dummy_prop"
        prop_val = "true"
        try:
            device.setprop(prop_name, prop_val)
        except simpleadb.AdbCommandError as err:
            self.fail(err)
        self.assertEqual(prop_val, device.getprop(prop_name))

    @pytest.mark.skipif(
        is_github_workflows_env(), not enable_root_tests(), reason="Failing on emulator"
    )
    def test_verity(self):
        """Check if verity command is not failing."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        device.root()
        device.remount()
        try:
            device.enable_verity(True)
            device.enable_verity(False)
        except simpleadb.AdbCommandError as err:
            print("ERR: ", err)
            self.fail(err)

    def test_push_pull(self):
        """Verify if file exists after push/pull command."""
        filename = "dummy_file"
        dest = "/sdcard/"

        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        os.system("touch " + filename)
        try:
            device.push(filename, dest)
            os.remove(filename)
            self.assertFalse(os.path.isfile(filename))
            device.pull(dest + filename)
            self.assertTrue(os.path.isfile(filename))
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_remove(self):
        """Check if file was removed after rm command."""
        filename = "test_remove_dummy_file"
        dest = "/sdcard/"
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        os.system("touch " + filename)
        try:
            device.push(filename, dest)
            os.remove(filename)
            device.rm(dest + filename)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

        with self.assertRaises(simpleadb.AdbCommandError):
            device.pull(dest + filename)

    def test_remove_not_existing_file_failure(self):
        """Check if rm command failed if file not exists."""
        filename = "/sdcard/no_existing_file"
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        with self.assertRaises(simpleadb.AdbCommandError):
            device.rm(filename)

    def test_get_ip_is_correct_ip(self):
        """Check get ip from ifconfig command."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            ip_address = device.get_ip()
            self.assertTrue(is_valid_ip(ip_address))
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_get_ip_fails_when_wrong_interface(self):
        """Check get ip from ifconfig command from not existing interface."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        with self.assertRaises(simpleadb.AdbCommandError):
            device.get_ip("dummy_interface")

    def test_get_state_returns_correct_state(self):
        """Check adb get state command."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        state = device.get_state()
        self.assertEqual(state, "device")

    def test_get_state_when_id_wrong_failed(self):
        """Check adb get state command."""
        device = simpleadb.AdbDevice("wrong id")
        with self.assertRaises(simpleadb.AdbCommandError):
            device.get_state()

    def test_dump_logcat(self):
        """Test dump logcat."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        log = device.dump_logcat()
        self.assertNotEqual(log, None)

    def test_dump_logcat_from_buffer(self):
        """Test dump logcat."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        log = device.dump_logcat("main")
        self.assertNotEqual(log, None)

    def test_clear_logcat(self):
        """Test clear logcat."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.clear_logcat()
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_clear_logcat_buf(self):
        """Test clear logcat from main buffer."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.clear_logcat("main")
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    @pytest.mark.skipif(is_github_workflows_env(), reason="Failing on emulator")
    def test_device_is_available(self):
        """Test if device is available."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        self.assertTrue(device.is_available())

    def test_no_available(self):
        """Test if device not available."""
        device = simpleadb.AdbDevice("dummy_id")
        self.assertFalse(device.is_available())

    def test_wait_for_device(self):
        """Test wait for device."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.wait_for_device()
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_wait_for_device_failed(self):
        """Wait for device failed after timeout if device not exists."""
        with self.assertRaises(simpleadb.AdbCommandTimeoutExpired):
            device = simpleadb.AdbDevice("dummy-device")
            device.wait_for_device(1)

    def test_wait_for_device_timeout(self):
        """Test wait for device with custom timeout."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.wait_for_device(5)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_adb_shell(self):
        """Test adb shell input command."""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.shell("input text 42")
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    @pytest.mark.skipif(
        not enable_root_tests(), reason="Failing on not rootable devices"
    )
    def test_unroot(self):
        """Test unroot"""
        device = simpleadb.AdbDevice(TEST_DEVICE_ID)
        try:
            device.unroot()
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    @pytest.mark.skipif(not is_github_workflows_env(), reason="Failing on non emulator")
    def test_adb_connect_emulator_success(self):
        """Test adb connect to emulator."""
        try:
            device = simpleadb.AdbDevice("localhost", 5555)
            device.wait_for_device()
            simpleadb.AdbServer().disconnect("localhost")
        except simpleadb.AdbCommandError as err:
            self.fail(err)

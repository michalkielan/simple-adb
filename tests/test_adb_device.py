#!/bin/python3
import unittest
import os
import subprocess
import simpleadb

def get_test_device_id():
  return os.environ['TEST_DEVICE_ID']

def get_adb_path():
  return '/usr/local/android-sdk/platform-tools/adb'

TEST_DEVICE_ID = get_test_device_id()
DUMMY_APK_NAME = 'app-debug.apk'
DUMMY_PACKAGE_NAME = 'com.dummy_app.dummy'


class AdbDeviceTest(unittest.TestCase):
  def setUp(self):
    self.__adb = simpleadb.AdbServer()

  def tearDown(self):
    self.__adb.kill()

  def test_devices(self):
    devices = self.__adb.devices()
    if not devices:
      self.fail('No adb devices found')
    emulator = devices[0]
    self.assertTrue(TEST_DEVICE_ID in emulator.get_id())

  def test_device_eq(self):
    dev1 = simpleadb.AdbDevice('1234')
    dev2 = simpleadb.AdbDevice('1234')
    dev3 = simpleadb.AdbDevice('42')
    self.assertEqual(dev1, dev2)
    self.assertNotEqual(dev1, dev3)

  def test_str(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    self.assertEqual(TEST_DEVICE_ID, str(device))

  def test_custom_path(self):
    device = simpleadb.AdbDevice(
      TEST_DEVICE_ID,
      path=get_adb_path()
    )
    self.assertTrue(device.is_available())

  def test_custom_path_fail(self):
    device = simpleadb.AdbDevice(
      TEST_DEVICE_ID,
      path='dummy/path'
    )
    with self.assertRaises(subprocess.CalledProcessError):
      self.assertTrue(device.is_available())

  def test_aroot(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.root()
    self.assertEqual(res, 0)
    self.assertTrue(device.is_root())

  def test_get_id(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    test_device_id = device.get_id()
    self.assertEqual(test_device_id, TEST_DEVICE_ID)

  def test_get_serialno(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    test_device_id = device.get_serialno()
    self.assertEqual(test_device_id, TEST_DEVICE_ID)

  def test_tap(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    res = device.tap(1, 1)
    self.assertEqual(res, 0)

  def test_screencap(self):
    filepath = './screenshot.png'
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.screencap(local=filepath)
    device.screencap()
    self.assertEqual(res, 0)
    self.assertTrue(os.path.isfile(filepath))

  def test_install(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    device.remount()
    res = device.install(DUMMY_APK_NAME)
    self.assertEqual(res, 0)
    res = device.uninstall(DUMMY_PACKAGE_NAME)
    self.assertEqual(res, 0)

  def test_setprop(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    res = device.setprop("dummy_prop", "true")
    self.assertEqual(res, 0)

  def test_verity(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.root()
    device.remount()
    res = device.enable_verity(True)
    self.assertEqual(res, 0)
    res = device.enable_verity(False)
    self.assertEqual(res, 0)

  def test_push_pull(self):
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
    filename = '/sdcard/no_existing_file'
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)

    with self.assertRaises(subprocess.CalledProcessError):
      res = device.rm(filename)
      self.assertNotEqual(res, 0)

  def test_get_state(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    state = device.get_state()
    self.assertEqual(state, 'device')

  def test_available(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    if not device.is_root():
      device.root()
    self.assertTrue(device.is_available())

  def test_no_available(self):
    device = simpleadb.AdbDevice('dummy_id')
    self.assertFalse(device.is_available())

  def test_wait_for_device(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.wait_for_device()
    self.assertEqual(0, res)

  def test_wait_for_device_failed(self):
    with self.assertRaises(subprocess.TimeoutExpired):
      device = simpleadb.AdbDevice('dummy-device')
      device.wait_for_device(timeout=1)

  def test_wait_for_device_timeout(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.root()
    res = device.wait_for_device(timeout=5)
    self.assertEqual(0, res)

  def test_adb_shell(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.root()
    res = device.shell('input text 42')
    self.assertEqual(0, res)

  def test_unroot(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.unroot()
    self.assertEqual(res, 0)

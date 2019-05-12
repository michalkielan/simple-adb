import unittest
import os
import sys
import subprocess
import simpleadb

def get_test_device_id():
  try:
    return os.getenv('TEST_DEVICE_ID')
  except KeyError:
    sys.exit('TEST_DEVICE_ID not found export device id')

def clone_app():
  url = 'https://github.com/michalkielan/AndroidDummyApp.git'
  os.system('git clone ' + url)
  os.system('cd AndroidDummyApp')
  os.system('./gradlew build')
  os,system('cd ..')
  os.system('cp AndroidDummyApp/app/build/outputs/apk/debug/app-debug.apk .')

TEST_DEVICE_ID = get_test_device_id()
DUMMY_APK_NAME = 'app-debug.apk'
DUMMY_PACKAGE_NAME = 'com.dummy_app.dummy'


class AdbServerTest(unittest.TestCase):
  def test_devices(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    emulator = devices[0]
    self.assertTrue(TEST_DEVICE_ID in emulator.get_id())

  def test_root(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.root()
    self.assertEqual(res, 0)
    os.system('adb wait-for-device shell input keyevent 82')

  def test_get_id(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    test_device_id = device.get_id()
    self.assertEqual(test_device_id, TEST_DEVICE_ID)

  def test_get_serialno(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    test_device_id = device.get_serialno()
    self.assertEqual(test_device_id, TEST_DEVICE_ID)

  def test_tap(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.tap(1, 1)
    self.assertEqual(res, 0)

  def test_install(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.install(DUMMY_APK_NAME)
    self.assertEqual(res, 0)

  def test_uninstall(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.uninstall(DUMMY_PACKAGE_NAME)
    self.assertEqual(res, 0)

  def test_setprop(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.setprop("dummy_prop", "true")
    self.assertEqual(res, 0)

  def test_get_state(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    state = device.get_state()
    self.assertEqual(state, 'device')

  def test_available(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    self.assertTrue(device.is_available())

  def test_no_available(self):
    device = simpleadb.AdbDevice('dummy_id')
    self.assertFalse(device.is_available())

  def test_wait_for_device(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.wait_for_device()
    self.assertTrue(0, res)

  def test_wait_for_device_timeout(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    res = device.wait_for_device(timeout=1)
    self.assertTrue(0, res)

  def test_wait_for_device_failed(self):
    with self.assertRaises(subprocess.TimeoutExpired):
      device = simpleadb.AdbDevice('dummy-device')
      device.wait_for_device(timeout=1)

import unittest
import simpleadb
import os

TEST_DEVICE_ID = 'emulator-5554'
DUMMY_APK_NAME = 'app-debug.apk'
DUMMY_PACKAGE_NAME = 'com.dummy_app.dummy'

def clone_app():
  url = 'https://github.com/michalkielan/AndroidDummyApp.git'
  os.system('git clone ' + url)
  os.system('cd AndroidDummyApp')
  os.system('./gradlew build')
  os,system('cd ..')
  os.system('cp AndroidDummyApp/app/build/outputs/apk/debug/app-debug.apk .')

class AdbServerTest(unittest.TestCase):
  def test_devices(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    emulator = devices[0]
    self.assertTrue(TEST_DEVICE_ID in emulator.get_id())

  def test_root(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.root()
    os.system('adb wait-for-device shell input keyevent 82')

  def test_get_id(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    test_device_id = device.get_id()
    self.assertEqual(test_device_id, TEST_DEVICE_ID)

  def test_tap(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.tap(1, 1)

  def test_install(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.install(DUMMY_APK_NAME)

  def test_uninstall(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.uninstall(DUMMY_PACKAGE_NAME)

  def test_setprop(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.setprop("dummy_prop", "true")

  def test_available(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    self.assertTrue(device.is_available())

  def test_no_available(self):
    device = simpleadb.AdbDevice('dummy_id')
    self.assertFalse(device.is_available())

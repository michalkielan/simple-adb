import unittest
import simpleadb

TEST_DEVICE_ID = 'emulator-5554'
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
    device.root()

  def test_tap(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.tap(1, 1)

  def test_install(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.install(DUMMY_APK_NAME)

  def test_uninstall(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.install(DUMMY_PACKAGE_NAME)

  def test_setprop(self):
    device = simpleadb.AdbDevice(TEST_DEVICE_ID)
    device.setprop("dummy_prop", "true")

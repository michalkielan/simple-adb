import unittest
import simpleadb

DUMMY_APK_NAME = 'app-debug.apk'

def get_emulator_id():
  return 'emulator-5554'

class AdbServerTest(unittest.TestCase):
  def test_devices(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    emulator = devices[0]
    self.assertTrue(get_emulator_id() in emulator.get_id())

  def test_root(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.root()

  def test_tap(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.tap(1, 1)

  def test_install(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.install(DUMMY_APK_NAME)

  def test_setprop(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.setprop("dummy_prop", "true")

import unittest
import simpleadb

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

  def test_broadcat(self):
    pass

  def test_setprop(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.setprop("dummy_prop", "true")

  def test_push(self):
    pass

  def test_pull(self):
    pass

  def test_unroot(self):
    device = simpleadb.AdbDevice(get_emulator_id())
    device.unroot()

  def test_reboot(self):
    pass

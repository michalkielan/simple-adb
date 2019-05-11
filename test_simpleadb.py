import simpleadb
import unittest

def get_emulator_id():
  return 'emulator-5554'

class AdbServerTest(unittest.TestCase):
  def test_devices(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    self.assertTrue(get_emulator_id() in devices[0].get_id())

  def test_root(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    for device in devices:
      device.root()

  def test_tap(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    for device in devices:
      device.tap(1, 1)

  def test_broadcat(self):
    pass

  def test_setprop(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    for device in devices:
      device.setprop("dummy_prop", "true")

  def test_push(self):
    pass

  def test_pull(self):
    pass

  def test_unroot(self):
    adb_server = simpleadb.AdbServer()
    devices = adb_server.devices()
    for device in devices:
      device.unroot()

  def test_reboot(self):
    pass

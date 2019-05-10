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

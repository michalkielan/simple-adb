import simpleadb
import unittest

def get_emulator_id():
  return 'emulator-5554'

class AdbServerTest(unittest.TestCase):
  def tst_adb_devices(self):
    adb_server = AdbServer()
    devices = adb_server.devices()
    self.assertEqual(devices[0].get_id(), get_emulator_id())

#!/bin/python3
import unittest
import simpleadb

def get_test_device_id():
  return 'emulator-5554'

TEST_DEVICE_ID = get_test_device_id()


class AdbServerTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_adb_devices(self):
    adb = simpleadb.AdbServer()
    devices = adb.devices()
    if not devices:
      self.fail('No adb devices found')
    emulator = devices[0]
    self.assertTrue(TEST_DEVICE_ID in emulator.get_id())



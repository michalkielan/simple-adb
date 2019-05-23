import unittest
import subprocess
import simpleadb
import simpleadb.adbprocess as adbprocess

class AdbProcessTest(unittest.TestCase):
  def setUp(self):
    self.__adb = simpleadb.AdbServer()

  def tearDown(self):
    self.__adb.kill()

  def test_call_success(self):
    adb_process = adbprocess.AdbProcess()
    res = adb_process.call('devices')
    self.assertEqual(res, 0)

  def test_call_failure(self):
    adb_process = adbprocess.AdbProcess()
    res = adb_process.call('invalid4r4j838r')
    self.assertNotEqual(res, 0)

  def test_check_call_success(self):
    adb_process = adbprocess.AdbProcess()
    res = adb_process.check_call('devices')
    self.assertEqual(res, 0)

  def test_check_call_failure(self):
    adb_process = adbprocess.AdbProcess()
    with self.assertRaises(subprocess.CalledProcessError):
      adb_process.check_call('invalid4r4j838r')

  def test_check_output_success(self):
    adb_process = adbprocess.AdbProcess()
    try:
      output = adb_process.check_output('devices')
      self.assertNotNote(output, 0)
    except subprocess.CalledProcessError:
      self.fail('Failes, CalledProcessError raised')

  def test_check_output_failure(self):
    adb_process = adbprocess.AdbProcess()
    with self.assertRaises(subprocess.CalledProcessError):
      adb_process.check_output('invalid4r4j838r')

"""Unit tests for adb subprocess"""
import unittest
import subprocess
import simpleadb
import simpleadb.adbprocess as adbprocess


class AdbProcessTest(unittest.TestCase):
    """Adb process unit tests"""

    def setUp(self):
        """Start adb server in each test"""
        self.__adb = simpleadb.AdbServer()

    def tearDown(self):
        """Kill adb server in each test"""
        self.__adb.kill()

    def test_call_success(self):
        """Check for call process success"""
        adb_process = adbprocess.AdbProcess()
        res = adb_process.call('devices')
        self.assertEqual(res, 0)

    def test_call_failure(self):
        """Check for call process failed"""
        adb_process = adbprocess.AdbProcess()
        res = adb_process.call('invalid4r4j838r')
        self.assertNotEqual(res, 0)

    def test_check_call_success(self):
        """Check for check call process success"""
        adb_process = adbprocess.AdbProcess()
        res = adb_process.check_call('devices')
        self.assertEqual(res, 0)

    def test_check_call_failure(self):
        """Check for check call process failed"""
        adb_process = adbprocess.AdbProcess()
        with self.assertRaises(subprocess.CalledProcessError):
            adb_process.check_call('invalid4r4j838r')

    def test_check_output_success(self):
        """Check for check call output process success"""
        adb_process = adbprocess.AdbProcess()
        try:
            output = adb_process.check_output('devices')
            self.assertIsNotNone(output)
        except subprocess.CalledProcessError:
            self.fail('Failed, CalledProcessError raised')

    def test_check_output_failure(self):
        """Check for check call output process failed"""
        adb_process = adbprocess.AdbProcess()
        with self.assertRaises(subprocess.CalledProcessError):
            adb_process.check_output('invalid4r4j838r')

#
# file test_adb_process.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb subprocess"""
import unittest
import subprocess
import simpleadb
from simpleadb import adbprocess


class AdbProcessTest(unittest.TestCase):
    """Adb process unit tests"""

    def setUp(self):
        """Start adb server in each test"""
        self.__adb = simpleadb.AdbServer()

    def tearDown(self):
        """Kill adb server in each test"""
        self.__adb.kill()

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

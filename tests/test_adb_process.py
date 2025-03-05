#
# file test_adb_process.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=no-member
"""Unit tests for adb subprocess."""

import unittest
import simpleadb
from simpleadb import adbprocess


class AdbProcessTest(unittest.TestCase):
    """Adb process unit tests."""

    def test_when_valind_commdn_check_output_success(self):
        """Check for check call output process success."""
        simpleadb.AdbServer()
        adb_process = adbprocess.AdbProcess()
        try:
            output = adb_process.check_output(["devices"])
            self.assertIsNotNone(output)
        except simpleadb.AdbCommandError as err:
            self.fail(err)

    def test_when_invalid_command_check_output_fails(self):
        """Check for check call output process failed."""
        adb_process = adbprocess.AdbProcess()
        with self.assertRaises(simpleadb.AdbCommandError):
            adb_process.check_output(["invalid4r4j838r"])

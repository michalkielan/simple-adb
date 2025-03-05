#
# file adbprocess.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""Interface for adb process"""
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
from typing import List, Optional
from . import adbcmds


class AdbCommandError(Exception):
    """Adb command error exception.

    Raised when adb command failed or the process returns a non-zero exit
    status.

    :param str device_id: Device ID or Host address.
    :param str output: Adb command process output.
    :param Optional[CalledProcessError] called_process_error: Process failed
        exception.
    """

    def __init__(
        self,
        device_id: str,
        output: str,
        called_process_error: Optional[CalledProcessError] = None,
    ):
        super().__init__()
        self.device_id = device_id
        self.called_process_error = called_process_error
        self.output = (
            called_process_error.output
            if (output is None and called_process_error is not None)
            else output
        )

    def __str__(self):
        return self.output


class AdbCommandTimeoutExpired(Exception):
    """Adb command timeout expired exception. Raised when adb command timeout
        expired.

    :param str device_id: Device ID or Host address.
    :param TimeoutExpired timeout_expired: Process failed.
    """

    def __init__(self, device_id: str, timeout_expired: TimeoutExpired):
        super().__init__()
        self.device_id = device_id
        self.timeout_expired = timeout_expired

    def __str__(self):
        return f'Command "{self.timeout_expired.cmd}" timed out after \
            {self.timeout_expired.timeout} seconds.'


class AdbProcess:
    """AdbProcess this class is used to call adb process.

    :param Optional[str] device_id: Device ID, used when called adb command on
        device.
    :param: adb_path (Optional[str]): adb path, default: 'adb'
    """

    def __init__(
        self, device_id: Optional[str] = None, adb_path: Optional[str] = adbcmds.ADB
    ):
        self.device_id = device_id
        self.adb_path = adb_path

    def create_use_on_device_arg(self) -> str:
        """Create use on device argument.

        :return: Concatenated string used for adb commands '-s <device_id>', or
            empty string.
        :rtype: str
        """
        return "-s " + str(self.device_id) if self.device_id is not None else ""

    def check_output(self, args: List[str], **kwargs) -> str:
        """Call adb subprocess.

        :param List[str] prop: Arguments.
        :keyword str timeout: Timeout in sec.
        :raise: AdbCommandError: When failed.
        :return: Process output.
        """
        cmd = []
        cmd_args = [self.adb_path]
        if self.device_id is not None:
            cmd_args += [self.create_use_on_device_arg()]
        cmd_args += args
        cmd = " ".join(cmd_args)
        kwargs.setdefault("shell", True)
        kwargs.setdefault("universal_newlines", True)
        kwargs.setdefault("stderr", subprocess.STDOUT)
        try:
            return subprocess.check_output(cmd, **kwargs).rstrip("\n\r")
        except CalledProcessError as err:
            raise AdbCommandError(self.device_id, None, err) from err
        except TimeoutExpired as err:
            raise AdbCommandTimeoutExpired(self.device_id, err) from err

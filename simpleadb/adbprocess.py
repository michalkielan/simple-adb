#
# file adbprocess.py
#
# SPDX-FileCopyrightText: (c) 2019 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Interface for adb process"""
import subprocess
from subprocess import CalledProcessError
from typing import Optional
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

    def __init__(self, device_id: str, output: str,
                 called_process_error: Optional[CalledProcessError] = None):
        super().__init__()
        self.device_id = device_id
        self.called_process_error = called_process_error
        self.output = called_process_error.output if (
            output is None and called_process_error is not None) else output

    def __str__(self):
        return self.output


class AdbProcess:
    """AdbProcess this class is used to call adb process

      Args:
        path (Optional[str]): adb path, default: 'adb'
      Returns:
        0 if success, otherwise error code
    """

    def __init__(self, path: Optional[str] = adbcmds.ADB):
        self.__adb_path = path

    def check_output(self, args: str, **kwargs) -> str:
        """ Call process

          Args:
            args (str): Arguments
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            self.__adb_path,
            args,
        ])
        kwargs.setdefault('shell', True)
        kwargs.setdefault('universal_newlines', True)
        kwargs.setdefault('stderr', subprocess.STDOUT)
        return subprocess.check_output(cmd, **kwargs)

#
# file adbdeviceprocess.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Python wrapper for adb protocol """
from . import adbprocess


def set_device(device_id: str) -> str:
    """ Set specific device to adb command

      Args:
        Device id
      Returns:
        String to set device id in adb command
    """
    return '-s ' + str(device_id)


class AdbDeviceProcess:
    """Wrapper for adbprocess for specific device

      Args:
        device_id (str): Device id
        adb_path (str): Adb binary path
    """

    def __init__(self, device_id: str, adb_path: str):
        self.__adb_process = adbprocess.AdbProcess(adb_path)
        self.__id = device_id

    def call(self, args: str) -> int:
        """ Call process on adb device

          Args:
            args (str): Arguments
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec
          Returns:
            0 if success, otherwise error code
        """
        cmd = ' '.join([
            set_device(self.__id),
            args,
        ])
        return self.__adb_process.call(cmd)

    def check_call(self, args: str) -> str:
        """ Call process on adb device

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
            set_device(self.__id),
            args,
        ])
        return self.__adb_process.check_call(cmd)

    def check_output(self, args: str) -> str:
        """ Call process on adb device

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
            set_device(self.__id),
            args,
        ])
        return self.__adb_process.check_output(cmd).rstrip('\n\r')

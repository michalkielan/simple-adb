#
# file adbdeviceprocess.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=too-few-public-methods

""" Python wrapper for adb protocol """
from . import adbprocess


def set_device(device_id: str) -> str:
    """ Set specific device to adb command.

    :param str device_id: Device id.
    :return: Concatenated string used for adb commands '-s <device_id>'.
    :rtype: str
    """
    return '-s ' + str(device_id)


class AdbDeviceProcess:
    """ Wrapper for adbprocess for specific device.

    :param str device_id: Device id.
    :param str adb_path: Adb binary path.
    """

    def __init__(self, device_id: str, adb_path: str):
        self.__adb_process = adbprocess.AdbProcess(adb_path)
        self.__id = device_id

    def check_output(self, args: str) -> str:
        """ Call process on adb device

        :param str args: Process call arguments.
        :keyword int timeout: Timeout in seconds.
        :raise: CalledProcessError: When failed.
        :return: Adb command output.
        :rtype: str
        """
        cmd = ' '.join([
            set_device(self.__id),
            args,
        ])
        return self.__adb_process.check_output(cmd).rstrip('\n\r')

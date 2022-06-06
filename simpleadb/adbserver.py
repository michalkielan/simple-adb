#
# file adbserver.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" Python wrapper for adb protocol """
from . import adbprocess
from . import adbcmds
from . import adbdevice


def get_encoding_format():
    """Return terminal encoding format

      Returns:
        Encoding format
    """
    return 'utf-8'


class AdbServer():
    """Class for server specific adb commands

      Args:
        port (Optional[int]): Port number
        **kwargs: Arbitrary keyword arguments
      Keyword Args:
        path (str): adb path
    """

    def __init__(self, port=None, **kwargs):
        options_path = kwargs.get('path')
        path = options_path if options_path else adbcmds.ADB

        self.__adbcaller = adbprocess.AdbProcess(path)
        self.start(port)

    def __check_call(self, args):
        return self.__adbcaller.check_call(args)

    def devices(self):
        """ List connected devices

          Returns:
            List of connected devices serial numbers
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.DEVICES
        output = self.__adbcaller.check_output(cmd)
        devices = []
        devices_list = output.splitlines()
        devices_list.pop(0)
        for line in devices_list:
            device = line.strip().split()
            if device:
                device_id = device[0].decode(
                    get_encoding_format()
                )
                devices.append(adbdevice.AdbDevice(device_id))
        return devices

    def start(self, port=None):
        """ Ensure that there is a server running

          Args:
            port (Optional[int]): Port (default: default adb server port)
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        port_arg = ''
        if port is not None:
            port_arg += ' '.join(['-P', str(port)])
        cmd = ' '.join([
            port_arg,
            adbcmds.START_SERVER,
        ])
        res = self.__check_call(cmd)
        return res

    def kill(self):
        """ Kill the server if it is running

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.KILL_SERVER
        return self.__check_call(cmd)

    def usb(self):
        """ Restart adb server listening on USB

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.USB
        return self.__check_call(cmd)

    def tcpip(self, port):
        """ Restart adb server listening on TCP on PORT

          Args:
            port (int): Port number
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.TCPIP,
            str(port)
        ])
        return self.__check_call(cmd)

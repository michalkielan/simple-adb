#
# file adbserver.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

""" This module includes AdbServer class used for adb server operations. """

from typing import List, Optional, Union
from . import adbprocess
from . import adbcmds
from . import adbdevice


class AdbServer:
    """ AdbServer in a class representation for adb server operations.

    :param Optional[int] port: Port, default is 5555.
    :keyword str path: Adb binary path.

    :Example:

    >>> import simpleadb
    >>> device = simpleadb.AdbServer(5555)
    >>> device = simpleadb.AdbDevice(5555, path='/usr/bin/adb')
    """

    def __init__(self, port: Optional[int] = None, **kwargs):
        options_path = kwargs.get('path')
        adb_path = options_path if options_path else adbcmds.ADB
        self.__adb_process = adbprocess.AdbProcess(adb_path)
        self.start(port)

    def __check_call(self, args: str) -> int:
        return self.__adb_process.check_call(args)

    def devices(self) -> List[str]:
        """ Get list connected adb devices.

        :raise CalledProcessError: When failed.
        :return: List of connected devices serial numbers.
        :rtype: List[str]

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.devices()
        ['emulator-5554']
        """
        cmd = adbcmds.DEVICES
        output = self.__adb_process.check_output(cmd)
        devices = []
        devices_list = output.splitlines()
        devices_list.pop(0)
        for line in devices_list:
            device = line.strip().split()
            if device:
                device_id = device[0]
                devices.append(adbdevice.AdbDevice(device_id))
        return devices

    def connect(self, address, port: Optional[Union[int, str]] = 5555):
        """ Connect a device via TCP/IP.

        :param str address: Host address.
        :param port (Optional[Union[int,str]]): Port, default 5555.
        :raise CalledProcessError: When failed.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.connect('192.168.42.42', 5555)
        """
        cmd = ' '.join([
            adbcmds.CONNECT,
            address,
            str(port),
        ])
        res = self.__check_call(cmd)
        return res

    def disconnect(
            self, address, port: Optional[Union[int, str]] = None) -> int:
        """ Disconnect from given TCP/IP device.

        :param address str: Host address.
        :param (Optional[Union[int, str] port]): Port.
        :raise CalledProcessError: When failed.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.connect('192.168.42.42', 5555)
        >>> adb_server.disconnect('192.168.42.42')
        """
        cmd = ' '.join([
            adbcmds.DISCONNECT,
            address,
            str(port),
        ])
        res = self.__check_call(cmd)
        return res

    def start(self, port: Optional[Union[int, str]] = None) -> int:
        """ Start adb and ensure that there is running.

        :param address str: Host address.
        :param (Optional[Union[int, str] port]): Port, default adb server port.
        :raise CalledProcessError: When failed.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.start()
        >>> adb_server.start(5037)
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

    def kill(self) -> int:
        """ Kill the server if it is running.

        :raise CalledProcessError: When failed.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.kill()
        """
        cmd = adbcmds.KILL_SERVER
        return self.__check_call(cmd)

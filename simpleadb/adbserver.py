#
# file adbserver.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

"""This module includes AdbServer class used for adb server operations."""

from typing import List, Optional, Union
from subprocess import CalledProcessError
from . import adbcmds
from . import adbdevice
from .adbprocess import AdbCommandError, AdbProcess


class AdbServer:
    """AdbServer in a class representation for adb server operations.

    :param Optional[int] port: Port, default is 5555.
    :keyword str path: Adb binary path.

    :Example:

    >>> import simpleadb
    >>> device = simpleadb.AdbServer(5555)
    >>> device = simpleadb.AdbDevice(5555, path='/usr/bin/adb')
    """

    def __init__(self, port: Optional[int] = None, **kwargs):
        options_path = kwargs.get("path")
        adb_path = options_path if options_path else adbcmds.ADB
        self.__adb_process = AdbProcess(None, adb_path)
        self.start(port)

    def devices(self) -> List[str]:
        """Get list connected adb devices.

        :raise: AdbCommandError: When failed.
        :return: List of connected devices serial numbers.
        :rtype: List[str]

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.devices()
        ['emulator-5554']
        """
        cmd = []
        cmd.append(adbcmds.DEVICES)
        try:
            output = self.__adb_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(None, None, err) from err
        devices = []
        devices_list = output.splitlines()
        devices_list.pop(0)
        for line in devices_list:
            device = line.strip().split()
            if device:
                device_id = device[0]
                devices.append(adbdevice.AdbDevice(device_id))
        return devices

    def connect(self, address, port: Optional[Union[int, str]] = 5555) -> None:
        """Connect a device via TCP/IP.

        :param str address: Host address.
        :param port (Optional[Union[int,str]]): Port, default 5555.
        :raise CalledProcessError: When failed.

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.connect('192.168.42.42', 5555)
        """
        cmd = []
        cmd.append(adbcmds.CONNECT)
        cmd.append(address)
        cmd.append(str(port))
        self.__adb_process.check_output(cmd)

    def disconnect(self, address, port: Optional[Union[int, str]] = None) -> None:
        """Disconnect from given TCP/IP device.

        :param address str: Host address.
        :param (Optional[Union[int, str] port]): Port.
        :raise: AdbCommandError: When failed.

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.connect('192.168.42.42', 5555)
        >>> adb_server.disconnect('192.168.42.42')
        """
        cmd = []
        cmd.append(adbcmds.DISCONNECT)
        cmd.append(address + f":{port}" if port is not None else "")
        self.__adb_process.check_output(cmd)

    def start(self, port: Optional[Union[int, str]] = None) -> None:
        """Start adb and ensure that there is running.

        :param address str: Host address.
        :param (Optional[Union[int, str] port]): Port, default adb server port.
        :raise: AdbCommandError: When failed.

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.start()
        >>> adb_server.start(5037)
        """
        cmd = []
        if port is not None:
            cmd.append(" ".join(["-P", str(port)]))
        cmd.append(adbcmds.START_SERVER)
        try:
            self.__adb_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(None, None, err) from err

    def kill(self) -> None:
        """Kill the server if it is running.

        :raise: AdbCommandError: When failed.

        :Example:

        >>> import simpleadb
        >>> adb_server = simpleadb.AdbServer(5555)
        >>> adb_server.kill()
        """
        cmd = []
        cmd.append(adbcmds.KILL_SERVER)
        self.__adb_process.check_output(cmd)

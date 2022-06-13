#
# file adbdevice.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=too-many-public-methods

""" This module includes AdbDevice class used on device with given serial. """

import time
from subprocess import check_output, CalledProcessError, STDOUT
from typing import Optional, Union
from . import adbcmds
from . import adbdeviceprocess
from . import adbprocess
from .utils import is_valid_ip


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


class AdbDevice:
    """ AdbDevice is a class representation of adb commands used on device with
    given serial.

    :param str device_id: Device ID or Host address.
    :param Optional[int] port: Port, default is 5555.
    :keyword str path: Adb binary path.

    :example:

    >>> import simpleadb
    >>> device = simpleadb.AdbDevice('emulator-5554')
    >>> device = simpleadb.AdbDevice('emulator-5554', path='/usr/bin/adb')
    >>> device = simpleadb.AdbDevice('192.168.42.42', 5555)
    """

    def __init__(self, device_id: str, port: Optional[int] = None, **kwargs):
        options_path = kwargs.get('path')
        self.__adb_path = options_path if options_path else adbcmds.ADB
        if (port is not None or device_id ==
                'localhost' or is_valid_ip(device_id)):
            self.__id = (
                device_id + ":" + str(port) if port is not None else device_id)
            cmd = ' '.join([
                self.__adb_path,
                adbcmds.CONNECT,
                self.__id
            ])
            adbprocess.subprocess.check_call(cmd, shell=True, **kwargs)
        else:
            self.__id = device_id
        self.__adb_device_process = adbdeviceprocess.AdbDeviceProcess(
            self.__id,
            self.__adb_path
        )

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_id(self) -> str:
        """Get target device id. Return the device id used in constructor.

        :return: Device id.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_id()
        'emulator-5554'
        """
        return self.__id

    def get_state(self) -> str:
        """ Get device state. Print offline, bootloader or disconnect.

        :raise: AdbCommandError: When failed.
        :return: State offline, bootloader or device.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_state()
        'device'
        """
        cmd = adbcmds.GET_STATE
        try:
            return self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def get_app_pid(self, package_name: str) -> int:
        """ Return the PID of the application.

        :param str package_name: Package name.
        :raise: AdbCommandError: When failed.
        :return: Package PID.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_app_pid('com.dummy.app')
        4367
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            'pidof',
            package_name
        ])
        try:
            return int(self.__adb_device_process.check_output(cmd))
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def get_ip(self, interface: Optional[str] = 'wlan0') -> str:
        """ Return the device IP address.

        :param Optional[str] interface: Network interface, default wlan0.
        :raise: AdbCommandError: When failed.
        :return: Device ip address.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_ip('wlan0')
        '192.168.42.42'
        """
        if_config = (
            f"ifconfig {interface} | grep 'inet addr' | cut -d: -f2 | awk '{{print $1}}'"  # noqa: E501
        )
        cmd = ' '.join([
            adbcmds.SHELL,
            if_config
        ])
        try:
            output = self.__adb_device_process.check_output(cmd)
            if not is_valid_ip(output):
                raise AdbCommandError(self.get_id(), output, None)
            return output
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def get_serialno(self) -> str:
        """ Get target device serial number.

        :raise: AdbCommandError: When failed.
        :return: Serial number.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_serialno()
        'emulator-5554'
        """
        cmd = adbcmds.GET_SERIALNO
        try:
            return self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def is_available(self) -> bool:
        """ Check if device is available.

        :return: True if available, otherwise False.
        :rtype: bool

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.is_available()
        True
        """
        try:
            self.get_serialno()
            return True
        except AdbCommandError:
            return False

    def get_devpath(self) -> str:
        """ Get device path.

        :raise: AdbCommandError: When failed.
        :return: Device path.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_devpath()
        'usb:3383384308X'
        """
        cmd = adbcmds.DEVPATH
        try:
            return self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def remount(self) -> int:
        """ Remout partition read-write.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        >>> device.remount()
        """
        cmd = adbcmds.REMOUNT
        try:
            output = self.__adb_device_process.check_output(cmd)
            if 'remount failed' in output.lower():
                raise AdbCommandError(self.get_id(), output, None)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def reboot(self) -> int:
        """ Reboot the device. Defaults to booting system image.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.reboot()
        """
        cmd = adbcmds.REBOOT
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def root(
            self,
            timeout_sec: Optional[int] = None) -> None:
        """ Restart adb with root permission if device has one. Wait for device
        to be in 'device' state.

        :param Optional[int] timeout_sec: Timeout in seconds.
        :raise: AdbCommandError: When failed.
        :raise TimeoutExpired: When timeout.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        """
        cmd = adbcmds.ROOT
        try:
            output = self.__adb_device_process.check_output(cmd)
            if ('cannot' or 'unable') in output.lower():
                raise AdbCommandError(self.get_id(), output)
            self.wait_for_device(timeout_sec)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def unroot(
            self,
            timeout_sec: Optional[int] = None) -> None:
        """ Restart adb without root permission.

        :param Optional[int] timeout_sec: Timeout in seconds.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.unroot()
        """
        cmd = adbcmds.UNROOT
        try:
            self.__adb_device_process.check_output(cmd)
            self.wait_for_device(timeout_sec)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def is_root(self) -> bool:
        """ Check if device has root permissions (experimental). Not guarantee
        to work 'su' must be installed on device.

        :return: True if device is rooted, False otherwise.
        :rtype: bool

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        >>> device.is_root()
        True
        """
        try_su = 'su 0 id -u 2>/dev/null'
        cmd = ' '.join([
            adbcmds.SHELL,
            try_su,
        ])
        try:
            self.__adb_device_process.check_output(cmd)
            return True
        except CalledProcessError:
            return False

    def install(self, apk: str) -> None:
        """ Push package to the device and install.

        :param str apk: Package path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.install('dummy.apk')
        """
        cmd = ' '.join([
            adbcmds.INSTALL,
            apk,
        ])
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def uninstall(self, package: str) -> None:
        """ Remove app package from the device.

        :param str apk: Package name.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.uninstall('dummy.apk')
        """
        cmd = ' '.join([
            adbcmds.UNINSTALL,
            package,
        ])
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def shell(self, args: str) -> None:
        """ Run remote shell command interface.

        :param str args: Adb shell arguments.
        :raise: AdbCommandError: When failed.
        :return: Serial number.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.shell('ls')
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            args,
        ])
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def rm(self, remote_path: str) -> None:  # pylint: disable=invalid-name
        """ Remove file in adb device.

        :param str remote_path: Remote path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.rm('/sdcard/dummy_file')
        """
        cmd = ' '.join([
            adbcmds.RM,
            remote_path,
        ])
        self.shell(cmd)

    def tap(self, pos_x: int, pos_y: int) -> None:
        """ Tap screen.

        :param int pos_x: x position.
        :param int pos_y: y position.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.tap(42, 42)
        """
        cmd = ' '.join([
            adbcmds.INPUT_TAP,
            str(pos_x),
            str(pos_y),
        ])
        return self.shell(cmd)

    def swipe(self, pos_x1: int, pos_y1: int,
              pos_x2: int, pos_y2: int) -> None:
        """ Swipe screen.

        :param: int pos_x1: Start x position.
        :param: int pos_y1: Start y position.
        :param: int pos_x2: End x position.
        :param: int pos_y2: End y position.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.swipe(0, 0, 42, 42)
        """
        cmd = ' '.join([
            adbcmds.INPUT_SWIPE,
            str(pos_x1),
            str(pos_y1),
            str(pos_x2),
            str(pos_y2),
        ])
        return self.shell(cmd)

    def screencap(self, **kwargs) -> None:
        """ Capture screenshot.

        :keyword str remote: Remote path.
        :keyword str local: Local path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.screencap()
        """
        remote_default = '/sdcard/screencap.png'
        local_default = 'screencap'
        local_default += time.strftime("%Y%m%d-%H%M%S")
        local_default += '.png'

        remote_arg = kwargs.get('remote')
        local_arg = kwargs.get('local')

        remote = remote_arg if remote_arg else remote_default
        local = local_arg if local_arg else local_default

        cmd = ' '.join([
            adbcmds.SCREENCAP,
            remote
        ])
        self.shell(cmd)
        self.pull(remote, local)
        self.rm(remote)

    def broadcast(self, intent: str) -> int:
        """ Send broadcast.

        :param str intent: Intent argument.
        :return: 0 if success, error code otherwise.
        :raises: CalledProcessError: When failed.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.broadcast('am dummy_intent')
        """
        cmd = ' '.join([
            'am broadcast -a',
            intent,
        ])
        return self.shell(cmd)

    def pm_grant(self, package: str, permission: str) -> str:
        """ Grant permission.

        :param str package: Package name.
        :param str permission: Android permission.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.pm_grant('com.dummy.app', 'android.permission.PERMISSION')
        """
        cmd = ' '.join([
            adbcmds.PM_GRANT,
            package,
            permission,
        ])
        return self.shell(cmd)

    def setprop(self, prop: str, value: str) -> int:
        """Set property.

        :param str prop: Property name.
        :param str value: Property Value.
        :raise: CalledProcessError: When failed.
        :return: 0 if success, error code otherwise.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.setprop('persist.dummy_prop', 'true')
        """
        cmd = ' '.join([
            adbcmds.SETPROP,
            prop,
            value
        ])
        return self.shell(cmd)

    def getprop(self, prop: str) -> str:
        """ Get android system property value.

        :param str prop: Property name.
        :raise: CalledProcessError: When failed.
        :return: System property value.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.setprop('persist.dummy.prop 42')
        >>> device.getprop('persist.dummy.prop')
        '42'
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            adbcmds.GETPROP,
            prop,
        ])
        return self.__adb_device_process.check_output(cmd)

    def enable_verity(self, enabled: bool) -> None:
        """ Enable/Disable verity.

        :param bool enabled: If true enable verity, otherwise disable
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        >>> device.enable_verity(False)
        >>> device.remount()
        """
        cmd = (
            adbcmds.ENABLE_VERITY if enabled
            else adbcmds.DISABLE_VERITY
        )
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def push(self, source: str, dest: str) -> int:
        """ Copy local files/dirs to device.

        :param str source: Local path.
        :param str dest: Remote path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.push('dummy_file.txt', '/sdcard/Downloads/')
        """
        cmd = ' '.join([
            adbcmds.PUSH,
            source,
            dest,
        ])
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def pull(self, source: str, dest: Optional[str] = '.') -> None:
        """ Pull files or directories from remote device.

        :param str source: Remote path.
        :param Optional[str] dest: Local path, default is ``'.'``.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.push('dummy_file.txt', '/sdcard/Downloads/')
        >>> device.pull('/sdcard/Downloads/dummy_file.txt')
        >>> device.pull('/sdcard/Downloads/dummy_file.txt', '/tmp')
        """
        cmd = ' '.join([
            adbcmds.PULL,
            source,
            dest,
        ])
        try:
            return self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def wait_for_device(self, timeout_sec: Optional[int] = None) -> int:
        """ Wait for device available.

        :keyword int timeout: Timeout in sec, default 'inf'
        :raise: AdbCommandError: When failed.
        :raise TimeoutExpired: When timeout.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.wait_for_device()
        >>> device.wait_for_device(timeout=5)
        """
        cmd = ' '.join([
            self.__adb_path,
            '-s',
            self.get_id(),
            adbcmds.WAIT_FOR_DEVICE,
        ])
        try:
            check_output(cmd, shell=True, timeout=timeout_sec, stderr=STDOUT)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def dump_logcat(self, *buffers: str) -> str:
        """ Dump logcat.

        :param Optional[List[str]] buffers: List of logcat buffers to dump.
        :raise: AdbCommandError: When failed.
        :raise: TimeoutExpired: When timeout.
        :return: Logcat output string.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> dumped_logcat = device.dump_logcat()
        >>> main_logcat = device.dump_logcat('main')
        """
        cmd = ' '.join([
            adbcmds.LOGCAT,
        ])

        if buffers:
            buffers_cmd = [' ']
            for buf in buffers:
                buffers_cmd.append('-b')
                buffers_cmd.append(buf)
            cmd += ' '.join(buffers_cmd)

        cmd += ' -d'
        try:
            return self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def clear_logcat(self, *buffers: str) -> None:
        """ Clear logcat.

        :param Optional[List[str]] buffers: List of logcat buffers to clear.
        :raise: AdbCommandError: When failed.
        :raise: TimeoutExpired: When timeout.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.clear_logcat()
        >>> device.clear_logcat('main')
        """
        cmd = ' '.join([
            adbcmds.LOGCAT,
        ])

        if buffers:
            buffers_cmd = [' ']
            for buf in buffers:
                buffers_cmd.append('-b')
                buffers_cmd.append(buf)
            cmd += ' '.join(buffers_cmd)

        cmd += ' -c'
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def usb(self) -> None:
        """ Restart adb server listening on USB.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.usb()
        """
        cmd = adbcmds.USB
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

    def tcpip(self, port: Union[int, str]) -> None:
        """ Restart adb server listening on TCP on PORT.

        :param Union[[int, str] port: Port.
        :raise: AdbCommandError: When failed.
        :return: 0 if success, otherwise error code.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.tcpip(5555)
        """
        cmd = ' '.join([
            adbcmds.TCPIP,
            str(port)
        ])
        try:
            self.__adb_device_process.check_output(cmd)
        except CalledProcessError as err:
            raise AdbCommandError(self.get_id(), None, err) from err

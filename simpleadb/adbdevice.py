# pylint: disable=too-many-public-methods
#
# file adbdevice.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#


"""This module includes AdbDevice class used on device with given serial."""

import time
from typing import Optional, Union
from . import adbcmds
from . import adbprocess
from .adbprocess import AdbCommandError
from .utils import is_valid_ip


class AdbDevice:
    """AdbDevice is a class representation of adb commands used on device with
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
        options_path = kwargs.get("path")
        self.__adb_path = options_path if options_path else adbcmds.ADB
        if port is not None or device_id == "localhost" or is_valid_ip(device_id):
            self.__id = device_id + ":" + str(port) if port is not None else device_id
            cmd = " ".join([self.__adb_path, adbcmds.CONNECT, self.__id])
            adbprocess.subprocess.check_call(cmd, shell=True, **kwargs)
        else:
            self.__id = device_id
        self.__adb_process = adbprocess.AdbProcess(self.__id, self.__adb_path)

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
        """Get device state. Print offline, bootloader or disconnect.

        :raise: AdbCommandError: When failed.
        :return: State offline, bootloader or device.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_state()
        'device'
        """
        cmd = []
        cmd.append(adbcmds.GET_STATE)
        return self.__adb_process.check_output(cmd)

    def get_app_pid(self, package_name: str) -> int:
        """Return the PID of the application.

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
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append("pidof")
        cmd.append(package_name)
        return int(self.__adb_process.check_output(cmd))

    def get_ip(self, iface: Optional[str] = "wlan0") -> str:
        """Return the device IP address.

        :param Optional[str] iface: Network interface, default wlan0.
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
            f"ifconfig {iface} | grep 'inet addr' | cut -d: -f2 | awk '{{print $1}}'"
        )
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(if_config)
        output = self.__adb_process.check_output(cmd)
        if not is_valid_ip(output):
            raise AdbCommandError(self.get_id(), output, None)
        return output

    def get_serialno(self) -> str:
        """Get target device serial number.

        :raise: AdbCommandError: When failed.
        :return: Serial number.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_serialno()
        'emulator-5554'
        """
        cmd = []
        cmd.append(adbcmds.GET_SERIALNO)
        return self.__adb_process.check_output(cmd)

    def is_available(self) -> bool:
        """Check if device is available.

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
        """Get device path.

        :raise: AdbCommandError: When failed.
        :return: Device path.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.get_devpath()
        'usb:3383384308X'
        """
        cmd = []
        cmd.append(adbcmds.DEVPATH)
        return self.__adb_process.check_output(cmd)

    def remount(self) -> None:
        """Remout partition read-write.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        >>> device.remount()
        """
        cmd = []
        cmd.append(adbcmds.REMOUNT)
        output = self.__adb_process.check_output(cmd)
        if "remount failed" in output.lower():
            raise AdbCommandError(self.get_id(), output, None)

    def reboot(self) -> None:
        """Reboot the device. Defaults to booting system image.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.reboot()
        """
        cmd = []
        cmd.append(adbcmds.REBOOT)
        self.__adb_process.check_output(cmd)

    def root(self, timeout_sec: Optional[int] = None) -> None:
        """Restart adb with root permission if device has one. Wait for device
        to be in 'device' state.

        :param Optional[int] timeout_sec: Timeout in seconds.
        :raise: AdbCommandError: When failed.
        :raise TimeoutExpired: When timeout.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        """
        cmd = []
        cmd.append(adbcmds.ROOT)
        output = self.__adb_process.check_output(cmd)
        if ("cannot" or "unable") in output.lower():
            raise AdbCommandError(self.get_id(), output)
        self.wait_for_device(timeout_sec)

    def unroot(self, timeout_sec: Optional[int] = None) -> None:
        """Restart adb without root permission.

        :param Optional[int] timeout_sec: Timeout in seconds.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.unroot()
        """
        cmd = []
        cmd.append(adbcmds.UNROOT)
        self.__adb_process.check_output(cmd)
        self.wait_for_device(timeout_sec)

    def is_root(self) -> bool:
        """Check if device has root permissions (experimental). Not guarantee
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
        try_su = "su 0 id -u 2>/dev/null"
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(try_su)
        try:
            self.__adb_process.check_output(cmd)
            return True
        except AdbCommandError:
            return False

    def install(self, apk: str) -> None:
        """Push package to the device and install.

        :param str apk: Package path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.install('dummy.apk')
        """
        cmd = []
        cmd.append(adbcmds.INSTALL)
        cmd.append(apk)
        self.__adb_process.check_output(cmd)

    def uninstall(self, package: str) -> None:
        """Remove app package from the device.

        :param str apk: Package name.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.uninstall('dummy.apk')
        """
        cmd = []
        cmd.append(adbcmds.UNINSTALL)
        cmd.append(package)
        self.__adb_process.check_output(cmd)

    def shell(self, args: str) -> str:
        """Run remote shell command interface.

        :param str args: Adb shell arguments.
        :raise: AdbCommandError: When failed.
        :return: Serial number.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.shell('ls')
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(args)
        return self.__adb_process.check_output(cmd)

    def rm(self, remote_path: str) -> None:
        """Remove file in adb device.

        :param str remote_path: Remote path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.rm('/sdcard/dummy_file')
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.RM)
        cmd.append(remote_path)
        self.__adb_process.check_output(cmd)

    def tap(self, pos_x: int, pos_y: int) -> None:
        """Tap screen.

        :param int pos_x: x position.
        :param int pos_y: y position.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.tap(42, 42)
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.INPUT_TAP)
        cmd.append(str(pos_x))
        cmd.append(str(pos_y))
        self.__adb_process.check_output(cmd)

    def swipe(self, pos_x1: int, pos_y1: int, pos_x2: int, pos_y2: int) -> None:
        """Swipe screen.

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
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.INPUT_SWIPE)
        cmd.append(str(pos_x1))
        cmd.append(str(pos_y1))
        cmd.append(str(pos_x2))
        cmd.append(str(pos_y2))
        self.__adb_process.check_output(cmd)

    def screencap(self, **kwargs) -> None:
        """Capture screenshot.

        :keyword str remote: Remote path.
        :keyword str local: Local path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.screencap()
        """
        remote_default = "/sdcard/screencap.png"
        local_default = "screencap"
        local_default += time.strftime("%Y%m%d-%H%M%S")
        local_default += ".png"

        remote_arg = kwargs.get("remote")
        local_arg = kwargs.get("local")

        remote = remote_arg if remote_arg else remote_default
        local = local_arg if local_arg else local_default

        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.SCREENCAP)
        cmd.append(remote)
        self.__adb_process.check_output(cmd)
        self.pull(remote, local)
        self.rm(remote)

    def broadcast(self, intent: str) -> None:
        """Send broadcast.

        :param str intent: Intent argument.
        :raise: AdbCommandError: When failed.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.broadcast('am dummy_intent')
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append("am broadcast -a")
        cmd.append(intent)
        self.__adb_process.check_output(cmd)

    def pm_grant(self, package: str, permission: str) -> str:
        """Grant permission.

        :param str package: Package name.
        :param str permission: Android permission.
        :return: 0 if success, error code otherwise.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.pm_grant('com.dummy.app', 'android.permission.PERMISSION')
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.PM_GRANT)
        cmd.append(package)
        cmd.append(permission)
        self.__adb_process.check_output(cmd)

    def setprop(self, prop: str, value: str) -> None:
        """Set property.

        :param str prop: Property name.
        :param str value: Property Value.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.setprop('persist.dummy_prop', 'true')
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.SETPROP)
        cmd.append(prop)
        cmd.append(value)
        self.__adb_process.check_output(cmd)

    def getprop(self, prop: str) -> str:
        """Get android system property value.

        :param str prop: Property name.
        :raise: AdbCommandError: When failed.
        :return: System property value.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.setprop('persist.dummy.prop 42')
        >>> device.getprop('persist.dummy.prop')
        '42'
        """
        cmd = []
        cmd.append(adbcmds.SHELL)
        cmd.append(adbcmds.GETPROP)
        cmd.append(prop)
        return self.__adb_process.check_output(cmd)

    def enable_verity(self, enabled: bool) -> None:
        """Enable/Disable verity.

        :param bool enabled: If true enable verity, otherwise disable
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.root()
        >>> device.enable_verity(False)
        >>> device.remount()
        """
        cmd = []
        cmd.append((adbcmds.ENABLE_VERITY if enabled else adbcmds.DISABLE_VERITY))
        self.__adb_process.check_output(cmd)

    def push(self, source: str, dest: str) -> None:
        """Copy local files/dirs to device.

        :param str source: Local path.
        :param str dest: Remote path.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.push('dummy_file.txt', '/sdcard/Downloads/')
        """
        cmd = []
        cmd.append(adbcmds.PUSH)
        cmd.append(source)
        cmd.append(dest)
        self.__adb_process.check_output(cmd)

    def pull(self, source: str, dest: Optional[str] = ".") -> None:
        """Pull files or directories from remote device.

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
        cmd = []
        cmd.append(adbcmds.PULL)
        cmd.append(source)
        cmd.append(dest)
        return self.__adb_process.check_output(cmd)

    def wait_for_device(self, timeout_sec: Optional[int] = None) -> None:
        """Wait for device available.

        :keyword int timeout: Timeout in sec, default 'inf'
        :raise: AdbCommandError: When failed.
        :raise TimeoutExpired: When timeout.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.wait_for_device()
        >>> device.wait_for_device(timeout=5)
        """
        cmd = []
        cmd.append(adbcmds.WAIT_FOR_DEVICE)
        self.__adb_process.check_output(cmd, timeout=timeout_sec)

    def dump_logcat(self, *buffers: str) -> str:
        """Dump logcat.

        :param str \\*buffers: Additional logcat buffers to dump.
        :raise: AdbCommandError: When failed.
        :return: Logcat output string.
        :rtype: str

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> dumped_logcat = device.dump_logcat()
        >>> logcat = device.dump_logcat('main')
        >>> logcat = device.clear_logcat('main', 'kernel')
        """
        cmd = []
        cmd.append(adbcmds.LOGCAT)
        if buffers:
            for buf in buffers:
                cmd.append("-b")
                cmd.append(buf)
        cmd.append("-d")
        return self.__adb_process.check_output(cmd)

    def clear_logcat(self, *buffers: str) -> None:
        """Clear logcat.

        :param str \\*buffers: Additional logcat buffers to clear.
        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.clear_logcat()
        >>> device.clear_logcat('main')
        >>> device.clear_logcat('main', 'kernel')
        """
        cmd = []
        cmd.append(adbcmds.LOGCAT)

        if buffers:
            for buf in buffers:
                cmd.append("-b")
                cmd.append(buf)
        cmd.append("-c")
        self.__adb_process.check_output(cmd)

    def usb(self) -> None:
        """Restart adb server listening on USB.

        :raise: AdbCommandError: When failed.

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.usb()
        """
        cmd = []
        cmd.append(adbcmds.USB)
        self.__adb_process.check_output(cmd)

    def tcpip(self, port: Union[int, str]) -> None:
        """Restart adb server listening on TCP on PORT.

        :param Union[[int, str] port: Port.
        :raise: AdbCommandError: When failed.
        :return: 0 if success, otherwise error code.
        :rtype: int

        :example:

        >>> import simpleadb
        >>> device = simpleadb.AdbDevice('emulator-5554')
        >>> device.tcpip(5555)
        """
        cmd = []
        cmd.append(adbcmds.TCPIP)
        cmd.append(str(port))
        self.__adb_process.check_output(cmd)

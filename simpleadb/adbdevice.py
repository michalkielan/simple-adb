#
# file adbdevice.py
#
# SPDX-FileCopyrightText: (c) 2022 Michal Kielan
#
# SPDX-License-Identifier: GPL-3.0-only
#

# pylint: disable=too-many-public-methods

""" Python wrapper for adb protocol """
import time
from . import adbcmds
from . import adbdeviceprocess
from . import adbprocess
from .utils import is_valid_ip


class AdbDevice():
    """Class for device specific adb commands

       Args:
         device_id (str): Device ID or Host address
         port (Optional[str|int]): Port (default 5555)
         **kwargs: Arbitrary keyword arguments
       Keyword Args:
         path (str): adb path
    """

    def __init__(self, device_id, port=None, **kwargs):
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

    def get_id(self):
        """Get target device id

          Returns:
            Serial number
        """
        return self.__id

    def get_state(self):
        """Get state

         Returns:
            State: offline | bootloader | device
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.GET_STATE
        return self.__adb_device_process.check_output(cmd)

    def get_app_pid(self, package_name):
        """Get app pid

          Args:
            package_name (str): Package name
         Returns:
            App PID
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            'pidof',
            package_name
        ])
        return int(self.__adb_device_process.check_output(cmd))

    def get_serialno(self):
        """Get target device's serial number

          Returns:
            Serial number
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.GET_SERIALNO
        return self.__adb_device_process.check_output(cmd)

    def is_available(self):
        """ Check if device is available

          Returns:
            True if available otherwise False
        """
        try:
            self.get_serialno()
            return True
        except adbprocess.subprocess.CalledProcessError:
            return False

    def get_devpath(self):
        """ Get device path

          Returns:
            Device path
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.DEVPATH
        return self.__adb_device_process.check_output(cmd)

    def remount(self):
        """ Remout partition read-write

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.REMOUNT
        self.__adb_device_process.check_call(cmd)

    def reboot(self):
        """ Reboot the device

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.REBOOT
        self.__adb_device_process.check_call(cmd)

    def root(
            self,
            timeout_sec=None):
        """ Restart adb with root permission if device has one

          Args:
            timeout_sec (int): in sec (default 5s)
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
            TimeoutExpired: when timeout
        """
        cmd = adbcmds.ROOT
        res = self.__adb_device_process.check_call(cmd)
        if res == 0:
            return self.wait_for_device(timeout=timeout_sec)
        return res

    def unroot(
            self,
            timeout_sec=None):
        """ Restart adb without root permission

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.UNROOT
        res = self.__adb_device_process.check_call(cmd)
        if res == 0:
            return self.wait_for_device(timeout=timeout_sec)
        return res

    def is_root(self):
        """ Check if device has root permissions (experimental)

          Returns:
            True if rooted False if not
        """
        try_su = 'su 0 id -u 2>/dev/null'
        cmd = ' '.join([
            adbcmds.SHELL,
            try_su,
        ])
        res = self.__adb_device_process.call(cmd)
        if res == 0:
            return True
        return False

    def install(self, apk):
        """ Push package to the device and install

          Args:
            apk (str): Package path
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.INSTALL,
            apk,
        ])
        return self.__adb_device_process.check_call(cmd)

    def uninstall(self, package):
        """ Remove this app package from the device

          Args:
            package (str): Package name
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.UNINSTALL,
            package,
        ])
        return self.__adb_device_process.check_call(cmd)

    def shell(self, args):
        """Run remote shell command interface

          Args:
            args (str): Command
          Returns:
            Serial number
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            args,
        ])
        return self.__adb_device_process.check_call(cmd)

    def rm(self, remote):  # pylint: disable=invalid-name
        """Remove file in adb device

          Args:
            remote (str): Remote path
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.RM,
            remote,
        ])
        return self.shell(cmd)

    def tap(self, pos_x, pos_y):
        """ Tap screen

          Args:
            pos_x (int): x position
            pos_y (int): y position
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.INPUT_TAP,
            str(pos_x),
            str(pos_y),
        ])
        return self.shell(cmd)

    def swipe(self, pos_x1, pos_y1, pos_x2, pos_y2):
        """ Swipe screen

          Args:
            pos_x1 (int): start x position
            pos_y1 (int): start y position
            pos_x2 (int): end x position
            pos_y2 (int): end y position
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.INPUT_SWIPE,
            str(pos_x1),
            str(pos_y1),
            str(pos_x2),
            str(pos_y2),
        ])
        return self.shell(cmd)

    def screencap(self, **kwargs):
        """ Capture screenshot

          Args:
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            remote (str): remote path
            local (str): local path
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
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
        return 0

    def broadcast(self, intent):
        """ Send broadcast

          Args:
            intent (str): Intent args
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            'am broadcast -a',
            intent,
        ])
        return self.shell(cmd)

    def pm_grant(self, package, permission):
        """Grant permission

          Args:
            package (str): Package name
            permission (str): Android permission
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.PM_GRANT,
            package,
            permission,
        ])
        return self.shell(cmd)

    def setprop(self, prop, value):
        """Set property

          Args:
            prop (str): Property name
            value (str): Property Value
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.SETPROP,
            prop,
            value
        ])
        return self.shell(cmd)

    def getprop(self, prop):
        """Get android system property value

          Args:
            prop (str): Property name
          Returns:
            str: Property value
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.SHELL,
            adbcmds.GETPROP,
            prop,
        ])
        return self.__adb_device_process.check_output(cmd)

    def enable_verity(self, enabled):
        """Enable/Disable verity

          Args:
            enabled (bool): Enable: True - enable, False - disable
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = (
            adbcmds.ENABLE_VERITY if enabled
            else adbcmds.DISABLE_VERITY
        )
        return self.__adb_device_process.check_call(cmd)

    def push(self, source, dest):
        """Copy local files/dirs to device

          Args:
            source (str): Local path
            dest (str): Remote path
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.PUSH,
            source,
            dest,
        ])
        return self.__adb_device_process.check_call(cmd)

    def pull(self, source, dest='.'):
        """Copy local files/dirs from device

          Args:
            source (str): Remote path
            dest (Optional[str|int]): Local path default is '.'
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.PULL,
            source,
            dest,
        ])
        return self.__adb_device_process.check_call(cmd)

    def wait_for_device(self, **kwargs):
        """ Restart adb with root permission

          Args:
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec (default inf)
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
            TimeoutExpired: when timeout
        """
        cmd = ' '.join([
            self.__adb_path,
            '-s',
            self.get_id(),
            adbcmds.WAIT_FOR_DEVICE,
        ])
        return adbprocess.subprocess.check_call(cmd, shell=True, **kwargs)

    def dump_logcat(self, *buffers):
        """ Dump logcat

          Args:
            *buffers: List of logcat buffers to dump
          Returns:
            Logcat output string
          Raises:
            CalledProcessError: when failed
            TimeoutExpired: when timeout
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
        return self.__adb_device_process.check_output(cmd)

    def clear_logcat(self, *buffers):
        """ Clear logcat

          Args:
            *buffers: List of logcat buffers to dump
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
            TimeoutExpired: when timeout
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
        return self.__adb_device_process.check_call(cmd)

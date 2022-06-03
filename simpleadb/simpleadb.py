""" Python wrapper for adb protocol """
import time
from . import adbprocess  # pylint: disable=relative-beyond-top-level
from . import adbcmds  # pylint: disable=relative-beyond-top-level


def get_encoding_format():
    """Return terminal encoding format

      Returns:
        Encoding format
    """
    return 'utf-8'

# pylint: disable=too-many-public-methods


class AdbDevice(object):  # pylint: disable=useless-object-inheritance
    """Class for device specific adb commands

      Args:
        **kwargs: Arbitrary keyword arguments
      Keyword Args:
        path (str): adb path
    """

    def __init__(self, device_id, **kwargs):
        options_path = kwargs.get('path')
        path = options_path if options_path else adbcmds.ADB

        self.__adbcaller = adbprocess.AdbProcess(path)
        self.__id = device_id

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __call(self, args):
        cmd = ' '.join([
            adbcmds.get_set_device(self.get_id()),
            args,
        ])
        return self.__adbcaller.call(cmd)

    def __check_call(self, args):
        cmd = ' '.join([
            adbcmds.get_set_device(self.get_id()),
            args,
        ])
        return self.__adbcaller.check_call(cmd)

    def __check_output(self, args):
        cmd = ' '.join([
            adbcmds.get_set_device(self.get_id()),
            args,
        ])
        output = self.__adbcaller.check_output(cmd)
        decoded = output.decode(get_encoding_format())
        return decoded.rstrip("\n\r")

    def get_id(self):
        """Get target device id

          Returns:
            Serial number
        """
        return self.__id

    # scripting
    def get_state(self):
        """Get state

         Returns:
            State: offline | bootloader | device
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.GET_STATE
        return self.__check_output(cmd)

    def get_serialno(self):
        """Get target device's serial number

          Returns:
            Serial number
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.GET_SERIALNO
        return self.__check_output(cmd)

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
        return self.__check_output(cmd)

    def remount(self):
        """ Remout partition read-write

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.REMOUNT
        self.__check_call(cmd)

    def reboot(self):
        """ Reboot the device

          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = adbcmds.REBOOT
        self.__check_call(cmd)

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
        res = self.__check_call(cmd)
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
        res = self.__check_call(cmd)
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
        res = self.__call(cmd)
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
        return self.__check_call(cmd)

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
        return self.__check_call(cmd)

    # shell
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
        return self.__check_call(cmd)

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
        return self.__check_output(cmd)

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
        return self.__check_call(cmd)

    # file transfer
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
        return self.__check_call(cmd)

    def pull(self, source, dest='.'):
        """Copy local files/dirs from device

          Args:
            source (str): Remote path
            dest (Optional[str]): Local path default is '.'
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
        return self.__check_call(cmd)

    # networking
    def connect(self, ip_addess, port=5555):
        """Connect to a device via TCP/IP

          Args:
            ip_addess (str): Ip address
            port (Optional[str]): Port (default 5555)
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.CONNECT,
            ip_addess,
            str(port),
        ])
        return self.__check_call(cmd)

    def disconnect(self, ip_addess, port=5555):
        """Disconnect from given TCP/IP device

          Args:
            ip_addess (str): Ip address
            port (Optional[str]): Port (default 5555)
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            adbcmds.DISCONNECT,
            ip_addess,
            str(port),
        ])
        return self.__check_call(cmd)

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
            adbcmds.ADB,
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
        return self.__check_output(cmd)

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
        return self.__check_call(cmd)


class AdbServer(object):  # pylint: disable=useless-object-inheritance
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

    def __check_output(self, args):  # pylint: disable=unused-private-member
        output = self.__adbcaller.check_output(args)
        return output.decode(get_encoding_format())

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
                devices.append(AdbDevice(device_id))
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

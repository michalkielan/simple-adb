import adbprocess
import adbprefixes

def get_encoding_format():
  return 'utf-8'

def get_adb_restart_timeout_sec():
  return 5

# pylint: disable=too-many-public-methods
class AdbDevice(object):
  def __init__(self, device_id):
    self.__id = device_id

  def __check_call(self, args):
    cmd = ' '.join([
        adbprefixes.get_set_device(self.get_id()),
        args,
    ])
    return adbprocess.check_call(cmd)

  def __check_output(self, args):
    cmd = ' '.join([
        adbprefixes.get_set_device(self.get_id()),
        args,
    ])
    output = adbprocess.check_output(cmd)
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
    cmd = adbprefixes.get_get_state()
    return self.__check_output(cmd)

  def get_serialno(self):
    """Get target device's serial number

      Returns:
        Serial number
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_get_serialno()
    return self.__check_output(cmd)

  def is_available(self):
    """ Check if device is available

      Returns:
        True if available False if not
      Raises:
        CalledProcessError: when failed
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
    cmd = adbprefixes.get_devpath()
    return self.__check_output(cmd)

  def remount(self):
    """ Remout partition read-write

      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_remount()
    self.__check_call(cmd)

  def reboot(self):
    """ Reboot the device

      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_reboot()
    self.__check_call(cmd)

  def root(
      self,
      timeout_sec=get_adb_restart_timeout_sec()):
    """ Restart adb with root permission

      Args:
        Timeout in sec (default 5s)
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
        TimeoutExpired: when timeout
    """
    cmd = adbprefixes.get_root()
    res = self.__check_call(cmd)
    if res == 0:
      return self.wait_for_device(timeout=timeout_sec)
    return res

  def unroot(
      self,
      timeout_sec=get_adb_restart_timeout_sec()):
    """ Restart adb without root permission

      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_unroot()
    res = self.__check_call(cmd)
    if res == 0:
      return self.wait_for_device(timeout=timeout_sec)
    return res

  def usb(self):
    cmd = adbprefixes.get_usb()
    return self.__check_call(cmd)

  def install(self, apk):
    """ Push package to the device and install

      Args:
        Package path
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_install(),
        apk,
    ])
    return self.__check_call(cmd)

  def uninstall(self, package):
    """ Remove this app package from the device

      Args:
        Package name
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_uninstall(),
        package,
    ])
    return self.__check_call(cmd)

  #shell
  def shell(self, args):
    """Run remote shell command interface

      Args:
        Command
      Returns:
        Serial number
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_shell(),
        args,
    ])
    return self.__check_call(cmd)

  def tap(self, x, y):
    """ Tap screen

      Args:
        x: x position
        y: y position
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_input_tap(),
        str(x),
        str(y),
    ])
    return self.shell(cmd)

  def broadcast(self, intent):
    """ Send broadcast

      Args:
        Intent args
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        'am broadcast -a',
        params,
    ])
    return self.shell(cmd)

  def pm_grant(self, package, permission):
    """Grant permission

      Args:
        Package name
        Android permission
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_pm_grant(),
        package,
        permission,
    ])
    return self.shell(cmd)

  def setprop(self, prop, value):
    """Set property

      Args:
        Property name
        Property Value
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        'setprop',
        prop,
        value
    ])
    return self.shell(cmd)

  def getprop(self, prop):
    """Get property

      Args:
        Property name
      Returns:
        Property value
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        'getprop',
        prop,
    ])
    return self.shell(cmd)

  #file transfer
  def push(self, source, dest):
    """Copy local files/dirs to device

      Args:
        Local path
        Remote path
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_push(),
        source,
        dest,
    ])
    return self.__check_call(cmd)

  def pull(self, source, dest='.'):
    """Copy local files/dirs from device

      Args:
        Remote path
        Local path
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_pull(),
        source,
        dest,
    ])
    return self.__check_call(cmd)

  #networking
  def connect(self, ip, port=5555):
    """Connect to a device via TCP/IP

      Args:
        Ip address
        Port (default 5555)
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_connect(),
        ip,
        str(port),
    ])
    return self.__check_call(cmd)

  def disconnect(self, ip, port=5555):
    """Disconnect from given TCP/IP device

      Args:
        ip: Ip address
        port: Port (default 5555)
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_disconnect(),
        ip,
        str(port),
    ])
    return self.__check_call(cmd)

  def wait_for_device(self, **options):
    """ Restart adb with root permission

      Args:
        **options: timeout (default inf)
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
        TimeoutExpired: when timeout
    """
    cmd = ' '.join([
        adbprefixes.get_adb_prefix(),
        '-s',
        self.get_id(),
        adbprefixes.get_wait_for_device(),
    ])

    timeout_sec = options.get("timeout")
    if timeout_sec:
      return adbprocess.subprocess.check_call(
          cmd,
          shell=True,
          timeout=timeout_sec
      )
    return adbprocess.subprocess.check_call(cmd, shell=True)


class AdbServer(object):
  def __init__(self):
    pass

  @staticmethod
  def __check_call(args):
    return adbprocess.check_call(args)

  @staticmethod
  def __check_output(args):
    output = adbprocess.check_output(args)
    return output.decode(get_encoding_format())

  @staticmethod
  def devices():
    """ List connected devices

      Returns:
        List of connected devices serial numbers
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_devices()
    output = adbprocess.check_output(cmd)
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

  def kill(self):
    """ Kill the server if it is running

      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_kill_server()
    return self.__check_call(cmd)

  def tcpip(self, port):
    """ Restart adb server listening on TCP on PORT

      Args:
        Port
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_tcpip(),
        str(port)
    ])
    return self.__check_call(cmd)

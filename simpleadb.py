import adbprocess
import adbprefixes

def get_encoding_format():
  return 'utf-8'

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
    return output.decode(get_encoding_format())

  def get_id(self):
    return self.__id

  # scripting
  def get_state(self):
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

  def root(self):
    """ Restart adb with root permission
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_root()
    return self.__check_call(cmd)

  def unroot(self):
    """ Restart adb without root permission
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = adbprefixes.get_unroot()
    return self.__check_call(cmd)

  def usb(self):
    cmd = adbprefixes.get_usb()
    return self.__check_call(cmd)

  def install(self, apk):
    """ Install package
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
    """ Uninstall package 
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
  def tap(self, x, y):
    """ Tap
      Args:
        x: x position
        y: y position
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_shell(),
        adbprefixes.get_input_tap(),
        str(x),
        str(y),
    ])
    return self.__check_call(cmd)

  def broadcast(self, intent):
    """ Send broadcast
      Args:
        intent
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        adbprefixes.get_shell(),
        'am broadcast -a',
        params,
    ])
    return self.__check_call(cmd)

  def pm_grant(self, package, permission):
    cmd = ' '.join([
        adbprefixes.get_shell(),
        adbprefixes.get_pm_grant(),
        package,
        permission,
    ])
    return self.__check_call(cmd)

  def setprop(self, prop, value):
    cmd = ' '.join([
        adbprefixes.get_shell(),
        'setprop',
        prop,
        value
    ])
    return self.__check_call(cmd)

  def getprop(self, prop):
    cmd = ' '.join([
        adbprefixes.get_shell(),
        'getprop',
        prop,
    ])
    return self.__check_output(cmd)

  #file transfer
  def push(self, source, dest):
    cmd = ' '.join([
        adbprefixes.get_push(),
        source,
        dest,
    ])
    return self.__check_call(cmd)

  def pull(self, source, dest='.'):
    cmd = ' '.join([
        adbprefixes.get_pull(),
        source,
        dest,
    ])
    return self.__check_call(cmd)

  #networking
  def connect(self, ip, port=5555):
    cmd = ' '.join([
        adbprefixes.get_connect(),
        ip,
        str(port),
    ])
    return self.__check_call(cmd)

  def disconnect(self, ip, port=5555):
    cmd = ' '.join([
        adbprefixes.get_disconnect(),
        ip,
        str(port),
    ])
    return self.__check_call(cmd)


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
    cmd = adbprefixes.get_kill_server()
    return self.__check_call(cmd)

  def tcpip(self, port):
    cmd = ' '.join([
        adbprefixes.get_tcpip(),
        str(port)
    ])
    return self.__check_call(cmd)

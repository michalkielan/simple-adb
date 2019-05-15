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
    return self.__id

  # scripting
  def get_state(self):
    cmd = adbprefixes.get_get_state()
    return self.__check_output(cmd)

  def get_serialno(self):
    cmd = adbprefixes.get_get_serialno()
    return self.__check_output(cmd)

  def is_available(self):
    try:
      self.get_serialno()
      return True
    except adbprocess.subprocess.CalledProcessError:
      return False

  def get_devpath(self):
    cmd = adbprefixes.get_devpath()
    return self.__check_output(cmd)

  def remount(self):
    cmd = adbprefixes.get_remount()
    self.__check_call(cmd)

  def reboot(self):
    cmd = adbprefixes.get_reboot()
    self.__check_call(cmd)

  def root(
      self,
      timeout_sec=get_adb_restart_timeout_sec()):
    cmd = adbprefixes.get_root()
    res = self.__check_call(cmd)
    if res == 0:
      return self.wait_for_device(timeout=timeout_sec)
    return res

  def unroot(
      self,
      timeout_sec=get_adb_restart_timeout_sec()):
    cmd = adbprefixes.get_unroot()
    res = self.__check_call(cmd)
    if res == 0:
      return self.wait_for_device(timeout=timeout_sec)
    return res

  def install(self, apk):
    cmd = ' '.join([
        adbprefixes.get_install(),
        apk,
    ])
    return self.__check_call(cmd)

  def uninstall(self, package):
    cmd = ' '.join([
        adbprefixes.get_uninstall(),
        package,
    ])
    return self.__check_call(cmd)

  #shell
  def shell(self, args):
    cmd = ' '.join([
        adbprefixes.get_shell(),
        args,
    ])
    return self.__check_call(cmd)

  def tap(self, x, y):
    cmd = ' '.join([
        adbprefixes.get_input_tap(),
        str(x),
        str(y),
    ])
    return self.shell(cmd)

  def broadcast(self, params):
    cmd = ' '.join([
        'am broadcast -a',
        params,
    ])
    return self.shell(cmd)

  def pm_grant(self, package, permission):
    cmd = ' '.join([
        adbprefixes.get_pm_grant(),
        package,
        permission,
    ])
    return self.shell(cmd)

  def setprop(self, prop, value):
    cmd = ' '.join([
        'setprop',
        prop,
        value
    ])
    return self.shell(cmd)

  def getprop(self, prop):
    cmd = ' '.join([
        'getprop',
        prop,
    ])
    return self.shell(cmd)

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

  def wait_for_device(self, **options):
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
  def __init__(self, port=None):
    self.start(port)

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

  def start(self, port=None):
    port_arg = ''
    if port is not None:
      port_arg += ' '.join(['-P', str(port)])
    cmd = ' '.join([
        port_arg,
        adbprefixes.get_start_server(),
    ])
    res = self.__check_call(cmd)
    return res

  def kill(self):
    cmd = adbprefixes.get_kill_server()
    return self.__check_call(cmd)

  def usb(self):
    cmd = adbprefixes.get_usb()
    return self.__check_call(cmd)

  def tcpip(self, port):
    cmd = ' '.join([
        adbprefixes.get_tcpip(),
        str(port)
    ])
    return self.__check_call(cmd)

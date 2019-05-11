import adbprocess

def get_encoding_format():
  return 'utf-8'

class AdbDevice():
  def __init__(self, device_id):
    self.__id = device_id

  def __check_call(self, args):
    cmd = ''
    cmd += '-s '
    cmd += str(self.get_id())
    cmd += ' '
    cmd += args
    return adbprocess.check_call(cmd)

  def __check_output(self, args):
    cmd = ''
    cmd += '-s '
    cmd += str(self.get_id())
    cmd += ' '
    cmd += args
    output = adbprocess.check_output(cmd)
    return output.decode(get_encoding_format())

  def get_id(self):
    return self.__id

  # scripting
  def get_state(self):
    cmd = 'get-state'
    output = adbprocess.check_output(cmd)
    return output.decode(get_encoding_format())

  def get_serialno(self):
    cmd = 'get-serialno'
    output = adbprocess.check_output(cmd)
    return output.decode(get_encoding_format())

  def get_serialno(self):
    cmd = 'get-devpath'
    output = adbprocess.check_output(cmd)
    return output.decode(get_encoding_format())

  def remount(self):
    cmd = 'remount'
    self.__check_call(cmd)

  def reboot(self):
    cmd = 'reboot'
    self.__check_call(cmd)

  def root(self):
    cmd = 'root'
    return self.__check_call(cmd)

  def unroot(self):
    cmd = 'unroot'
    return self.__check_call(cmd)

  def usb(self):
    cmd = 'usb'
    return self.__check_call(cmd)

  #shell
  def tap(self, x, y):
    cmd = ''
    cmd += 'shell input tap '
    cmd += str(x)
    cmd += ' '
    cmd += str(y)
    return self.__check_call(cmd)

  def broadcast(self, params):
    cmd = ''
    cmd = 'shell am broadcast -a '
    cmd += params
    return self.__check_call(cmd)

  def pm_grant(self, package, permission):
    cmd = ''
    cmd += 'shell pm grant '
    cmd += package
    cmd += ' '
    cmd += permission
    return self.__check_call(cmd)

  def setprop(self, prop, value):
    cmd = ''
    cmd = 'shell setprop '
    cmd += prop
    cmd += ' '
    cmd += value
    return self.__check_call(cmd)

  def getprop(self, prop):
    cmd = ''
    cmd = 'shell getprop '
    cmd += prop
    return self.__check_output(cmd)

  #file transfer
  def push(self, source, dest):
    cmd = ''
    cmd += 'push '
    cmd += source
    cmd += ' '
    cmd += dest
    return self.__check_call(cmd)

  def pull(self, source, dest='.'):
    cmd = ''
    cmd += 'pull '
    cmd += source
    cmd += ' '
    cmd += dest
    return self.__check_call(cmd)

  #networking
  def connect(self, ip, port=555):
    cmd = ''
    cmd += 'connect '
    cmd += ip
    cmd += ' '
    cmd += str(port)
    return self.__check_call(cmd)

  def disconnect(self, ip, port=555):
    cmd = ''
    cmd += 'diconnect '
    cmd += ip
    cmd += ' '
    cmd += str(port)
    return self.__check_call(cmd)


class AdbServer():
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
    cmd = 'devices'
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
    cmd = 'kill-server'
    return self.__check_call(cmd)

  def tcpip(self, port):
    cmd = ''
    cmd += 'tcpip '
    cmd += str(port)
    return self.__check_call(cmd)

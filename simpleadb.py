import adbprocess

def get_encoding_format():
  return 'utf-8'

class AdbDevice:
  def __init__(self, device_id):
    self.__id = device_id

  def __call(self, args):
    cmd = ''
    cmd += '-s '
    cmd += str(self.__get_id())
    cmd += ' '
    cmd += args
    return adbprocess.check_call(cmd)

  def get_id(self):
    return self.__id

  # scripting
  def reboot(self):
    cmd = 'reboot'
    self.__call(cmd)

  def root(self):
    cmd = 'root'
    return self.__call(cmd)

  #shell
  def tap(self, x, y):
    cmd = ''
    cmd += 'shell input tap '
    cmd += str(x)
    cmd += ' '
    cmd += str(y)
    return self.__call(cmd)

  def broadcast(self, params):
    cmd = ''
    cmd = 'shell am broadcast -a '
    cmd += params
    return self.__call(cmd)

  def pm_grant(self, package, permission):
    cmd = ''
    cmd += 'shell pm grant '
    cmd += package
    cmd += ' '
    cmd += permission
    return self.__call(cmd)

  def setprop(self, param, value):
    cmd = ''
    cmd = 'shell setprop '
    cmd += param
    cmd += ' '
    cmd += value
    return self.__call(cmd)

  #file transfer
  def push(self, source, dest):
    cmd = ''
    cmd += 'push '
    cmd += source
    cmd += ' '
    cmd += dest
    return self.__call(cmd)

  def pull(self, source, dest='.'):
    cmd = ''
    cmd += 'pull '
    cmd += source
    cmd += ' '
    cmd += dest
    return self.__call(cmd)

  #networking
  def connect(self, ip, port=555):
    cmd = ''
    cmd += 'connect '
    cmd += ip
    cmd += ' '
    cmd += str(port)
    return self.__call(cmd)

  def disconnect(self, ip, port=555):
    cmd = ''
    cmd += 'diconnect '
    cmd += ip
    cmd += ' '
    cmd += str(port)
    return self.__call(cmd)

  def tcpip(self, port):
    cmd = ''
    cmd += 'tcpip '
    cmd += str(port)
    return self.__call(cmd)


class AdbServer:
  def devices(self):
    cmd = 'devices'
    output = adbprocess.check_output(cmd)
    devices = []
    devices_list = output.splitlines()
    devices_list.pop(0)
    for line in devices_list:
      device = line.strip().split()
      if len(device) != 0:
        device_id = device[0].decode(
            get_encoding_format()
        )
        devices.append(AdbDevice(device_id))
    return devices

  def kill(self):
    cmd = 'kill-server'
    adbprocess.call(cmd)

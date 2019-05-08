import adbprocess

def get_encoding_format():
  return 'utf-8'

class AdbDevice:
  def __init__(self, device_id):
    self.__id = device_id

  def get_id(self):
    return self.__id

  def reboot(self):
    cmd = 'reboot'
    adbprocess.call(cmd)

  def root(self):
    cmd = 'root'
    adbprocess.call(cmd)

  def tap(self, x, y):
    cmd = ''
    cmd += 'shell input tap ' 
    cmd += str(x) 
    cmd += ' ' 
    cmd += str(y)
    adbprocess.call(cmd)

  def broadcast(self, params):
    cmd = ''
    cmd = 'shell am broadcast -a '
    cmd += params
    adbprocess.call(cmd)

  def pm_grant(self, package, permission):
    cmd = ''
    cmd += 'shell pm grant '
    cmd += package
    cmd += ' '
    cmd += permission
    adbprocess.call(cmd)

  def setprop(self, param, value):
    cmd = ''
    cmd = 'shell setprop '
    cmd += param
    cmd += ' '
    cmd += value
    adbprocess.call(cmd)

  def push(self, source, dest):
    cmd = ''
    cmd += 'push '
    cmd += source
    cmd += ' '
    cmd += dest
    adbprocess.call(cmd)

  def pull(self, source, dest='.')
    cmd = ''
    cmd += 'pull '
    cmd += source
    cmd += ' '
    cmd += dest
    adbprocess.call(cmd)


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


def test():
  adb_server = AdbServer()
  devices = adb_server.devices()

  for device in devices:
    print(device.get_id())

test()

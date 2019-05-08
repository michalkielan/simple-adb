import os
import subprocess

def get_encoding_format():
  return 'utf-8'

class AdbProcess:
  def call(self, cmd):
    subprocess.call(['adb', cmd])

  def check_output(self, cmd):
    return subprocess.check_output(
            'adb ' + cmd,
            shell=True)

adb_process = AdbProcess()

class AdbDevice:
  def __init__(self, device_id):
    self.__id = device_id

  def get_id(self):
    return self.__id

  def reset(self):
    cmd = 'reset'
    adb_process.call(cmd)
    pass

  def root(self):
    cmd = 'root'
    adb_process.call(cmd)
    pass

  def tap(self, x, y):
    cmd = ''
    cmd += 'shell input tap ' 
    cmd += str(x) 
    cmd += ' ' 
    cmd += str(y)
    adb_process.call(cmd)

  def broadcast(self, params):
    cmd = ''
    cmd = 'shell am broadcast -a '
    cmd += params
    adb_process.call(cmd)

  def pm_grant(self, package, permission)
    cmd = ''
    cmd += 'shell pm grant '
    cmd += package
    cmd += ' '
    cmd += permission
    adb_process.call(cmd)

  def setprop(self, param, value):
    cmd = ''
    cmd = 'shell setprop '
    cmd += param
    cmd += ' '
    cmd += value
    adb_process.call(cmd)


class AdbServer:
  def devices(self):
    cmd = 'devices'
    output = adb_process.check_output(cmd)
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
    self.__adb_process.call(cmd)


def test():
  adb_server = AdbServer()
  devices = adb_server.devices()

  for device in devices:
    print(device.get_id())

test()

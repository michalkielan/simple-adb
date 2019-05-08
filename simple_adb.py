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
    pass

  def set_prop(self):
    pass


class AdbServer:
  def devices(self):
    devices = []
    output = adb_process.check_output('devices')
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
    self.__adb_process.call('kill-server')


def main():
  adb_server = AdbServer()
  devices = adb_server.devices()

  for device in devices:
    print(device.get_id())


main()

# simple adb
[![Travis CI](https://travis-ci.org/michalkielan/simple-adb.svg?branch=master)](https://travis-ci.org/michalkielan/simple-adb)

Python wrapper for adb protocol

## Example usage
```
$ python3
>>> import simpleadb
>>> adb_server = simpleadb.AdbServer()
>>> devices = adb_server.devices()
>>> emulator = devices[0]
>>> print(emulator.get_id())
emulator-5554
>>> emulator.root()
restarting adbd as root
0
>>> emulator.reboot()
```

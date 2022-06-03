# simple adb
[![PyPi version](https://img.shields.io/pypi/v/simpleadb?color=blue)](https://pypi.org/project/simpleadb)
[![Travis CI](https://travis-ci.org/michalkielan/simple-adb.svg?branch=master)](https://travis-ci.org/michalkielan/simple-adb)
[![Coverage Status](https://coveralls.io/repos/github/michalkielan/simple-adb/badge.svg?branch=master&service=github)](https://coveralls.io/github/michalkielan/simple-adb?branch=master)

> Object oriented python wrapper for adb protocol.

## Install
```
$ pip install simpleadb
```

## Usage

```Python
>>> import simpleadb
>>> adb_server = simpleadb.AdbServer()
>>> devices = adb_server.devices()
>>> emulator = devices[0]
>>> emulator
'emulator-5554'
>>> emulator.root()
restarting adbd as root
0
>>> emulator.reboot()
```

## License

[GPL3](./LICENSE)

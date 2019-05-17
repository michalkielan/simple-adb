# simple adb
[![Travis CI](https://travis-ci.org/michalkielan/simple-adb.svg?branch=master)](https://travis-ci.org/michalkielan/simple-adb)
[![Coverage Status](https://coveralls.io/repos/github/michalkielan/simple-adb/badge.svg?branch=master&service=github)](https://coveralls.io/github/michalkielan/simple-adb?branch=master)

> Python wrapper for adb protocol

## Install

`$ python setup.py install`

## Usage

```Python
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

## Contributing

* add more adb commads
* imrove existing setup
* improve tests in travis

## License

[GPL3](./LICENSE)

[Unreleased](https://github.com/michalkielan/simple-adb/compare/0.5.2...HEAD)
-----------------------------------------------------------------------------

[0.5.2](https://github.com/michalkielan/simple-adb/compare/0.5.1...0.5.2) - 2025-03-24
### Changed
- move env variables in deployment script

[0.5.1](https://github.com/michalkielan/simple-adb/compare/0.5.0...0.5.1) - 2025-03-24
--------------------------------------------------------------------------------------
### Changed
- attempt to fix pypi api token

[0.5.0](https://github.com/michalkielan/simple-adb/compare/0.4.1...0.5.0) - 2025-03-23
--------------------------------------------------------------------------------------

### Changed
- switch from python 3.12 to 3.13
- update actions/setup-python@v5
- update to macos-13

### Added
- dependency automation bot
- deployment automation

[0.4.1](https://github.com/michalkielan/simple-adb/compare/0.4.0...0.4.1) - 2024-11-17
--------------------------------------------------------------------------------------

### Changed
- fixed wrong type hints
- formatter: autopep8 -> black
- adb test VM from macos 11 to 12
- tests python version 3.6->3.8
- switch from python 3.8 to 3.11
- switch from python 3.11 to 3.12
- update codecov to v5
- migrate from setup.py to pyproject.toml
- update to checkout/v4

### Added
- pylint and flake8 configuration files

[0.4.0](https://github.com/michalkielan/simple-adb/compare/0.3.4...0.4.0) - 2022-06-15
--------------------------------------------------------------------------------------

### Added
- timeout expired exception
- export exception classess to __init__ module
- 3.10 builds
- basic API doc

### Changed
- merge adb process classes
- replace all subprocess: call,check_call to check_output
- update actions/setup-python@v4

### Removed
- AdbDeviceProcess class
- redundant try except block

[0.3.4](https://github.com/michalkielan/simple-adb/compare/0.3.3...0.3.4) - 2022-06-12
--------------------------------------------------------------------------------------

### Added
- automatic linter
- exception for adb commands failures
- adb device supported commands:
	- get ip address
- add unit tests:
  - exceptions
  - get pid
  - get ip
  - connect/disconnect

### Changed
- fix for adb disconnect
- fix get ip address

### Removed
- Deprecate travis

[0.3.3](https://github.com/michalkielan/simple-adb/compare/0.3.2...0.3.3) - 2022-06-10
--------------------------------------------------------------------------------------

### Added
- minor refactor
- add cache for AVD VM
- add return error to: 
  - adb root
  - adb remount
- move tcpip/usb from adbserver to adbdevice
- publish sphinx documentation

### Changed
- generating description in setup.py due to fd leak
- api version 27 in CI
- docstring format to reStructuredText (reST)

[0.3.2](https://github.com/michalkielan/simple-adb/compare/0.3.1...0.3.2) - 2022-06-07
--------------------------------------------------------------------------------------

### Added
- support for gihub workflows
- spdx headers
- sphinx documentation
- get app pid method

### Changed
- setup.py lint
- general modules refactor
- fix tests:
  - fix wrong custom adb path
- fixed TCP/IP object creation
- use default decoding when using subprocess.check_output


[0.3.1](https://github.com/michalkielan/simple-adb/compare/0.3.0...0.3.1) - 2022-06-03
--------------------------------------------------------------------------------------

### Changed
- Change README from .md to .rst

[0.3.0](https://github.com/michalkielan/simple-adb/compare/0.2.0...0.3.0) - 2022-06-03
--------------------------------------------------------------------------------------

### Added
- long description
- pypi link in readme
- added flake8 to CI linter
- Swipe command

### Changed
- use py.test instead of tox in travis
- updated pylint version
- remove some pylint warnings

### Removed
- tox-travis

[0.2.0](https://github.com/michalkielan/simple-adb/compare/0.1.0...0.2.0) - 2021-06-08
--------------------------------------------------------------------------------------

### Added
- docstring for pytest

### Changed
- pylint mode for tests in travis builds

### Fixed
- travis builds
- return correct string from getprop
- changelog doc view

### Removed
- coverage

0.1.0 - 2021-06-05
------------------

### Added

- process call wrapper
- adb device supported commands:
	- get id
  - get state
  - get serial number
  - is available
  - get devpath
  - remount
  - reboot
  - root
  - unroot
  - is root
  - usb
  - install
  - uninstall
  - tap screen
  - screencap
  - broadcast
  - pm grant
  - set prop
  - get prop
  - push
  - pull
  - connect
  - disconnect
  - wait for device
  - shell
  - enable verity
  - disable verity
  - rm
- adb server supported commands:
  - devices
  - kill server
  - tcpip
- custom adb binary path
- travis ci
- adb emulator in travis
- coverage

[Unreleased](https://github.com/michalkielan/simple-adb/compare/0.3.1...HEAD)
-----------------------------------------------------------------------------

[0.3.0](https://github.com/michalkielan/simple-adb/compare/0.3.0...0.3.1) - 2022-06-03
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

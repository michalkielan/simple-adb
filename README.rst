==========
simple adb
==========

.. image:: https://img.shields.io/pypi/v/simpleadb?color=blue
   :target: https://pypi.org/project/simpleadb
   :alt: PyPi version

.. image:: https://app.travis-ci.com/michalkielan/simple-adb.svg?branch=master   
   :target: https://app.travis-ci.com/michalkielan/simple-adb
   :alt: Travis CI

.. image:: https://coveralls.io/repos/github/michalkielan/simple-adb/badge.svg?branch=master&service=github   
   :target: https://coveralls.io/github/michalkielan/simple-adb?branch=master
   :alt: Coverage Status

  Object oriented python wrapper for adb protocol.

Install
=======

.. code-block::
  $ pip install simpleadb

Usage
=====

.. code-block:: python
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

License
=======

`GPL3 <https://github.com/michalkielan/simple-adb/blob/master/LICENSE>`_
[GPL3](./LICENSE)

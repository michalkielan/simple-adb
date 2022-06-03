simple adb
==========

|PyPi version| |Travis CI| |Coverage Status|

   Object oriented python wrapper for adb protocol.

Install
-------

::

   $ pip install simpleadb

Usage
-----

.. code:: python

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
-------

`GPL3 <./LICENSE>`__

.. |PyPi version| image:: https://img.shields.io/pypi/v/simpleadb?color=blue
   :target: https://pypi.org/project/simpleadb
.. |Travis CI| image:: https://app.travis-ci.com/michalkielan/simple-adb.svg?branch=master
   :target: https://app.travis-ci.com/michalkielan/simple-adb
.. |Coverage Status| image:: https://coveralls.io/repos/github/michalkielan/simple-adb/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/michalkielan/simple-adb?branch=master

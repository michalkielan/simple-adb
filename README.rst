simple adb
==========

|PyPi version| |Build| |Tests| |Codecov|

   Object oriented python wrapper for adb protocol.

Install
-------

To install the current release.

::

   $ pip install simpleadb

Usage
-----

Try your first program.

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

For more examples, see API `documentation <https://michalkielan.github.io/simple-adb/index.html#module-simpleadb.adbdevice>`_.

License
-------

`GPL3 <./LICENSE>`__

.. |PyPi version| image:: https://img.shields.io/pypi/v/simpleadb?color=blue
   :target: https://pypi.org/project/simpleadb
.. |Build| image:: https://github.com/michalkielan/simple-adb/actions/workflows/build.yml/badge.svg?branch=master
   :target: https://github.com/michalkielan/simple-adb/actions/workflows/build.yml?query=branch%3Amaster
.. |Tests| image:: https://github.com/michalkielan/simple-adb/actions/workflows/tests.yml/badge.svg?branch=master
   :target: https://github.com/michalkielan/simple-adb/actions/workflows/tests.yml?query=branch%3Amaster
.. |Codecov| image:: https://codecov.io/gh/michalkielan/simple-adb/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/michalkielan/simple-adb


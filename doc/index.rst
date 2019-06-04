..
   file index.rst

   SPDX-FileCopyrightText: (c) 2019 Michal Kielan

   SPDX-License-Identifier: GPL-3.0-only

   simple-adb documentation master file, created by
   sphinx-quickstart on Mon Jun  3 21:21:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simple-adb's documentation!
======================================

************
Introduction
************
Simple-adb (Simple android debug protocol) is an open-source GPL-3.0-licenced
object oriented python library that includes several adb operations. The
motivation is to create a library that will automate the adb operations of
android devices.

**simpleadb** has two main components that could be used in adb operations:
  * **AdbServer** - Object defining adb server operations.
  * **AdbDevice** - Object defining adb device specific operations.

************
API Concepts
************

simpleadb Namespace
"""""""""""""""""""
Every components are placed in the **simpleadb** namespace. Import is required
to access.

.. code-block:: python

  >>> import simpleadb
  >>> adb = simpleadb.AdbServer()

or

.. code-block:: python

  >>> from simpleadb import AdbServer
  >>> adb = AdbServer()


AdbServer component
"""""""""""""""""""
AdbServer includes adb server operations.

.. code-block:: python

  >>> import simpleadb
  >>> adb = simpleadb.AdbServer()
  >>> adb.kill()
  >>> port=5555
  >>> adb.start(port)


AdbDevice component
"""""""""""""""""""
AdbDevice includes device specific operations. The serial number is required as
a constructor argument.

.. code-block:: python

  >>> import simpleadb
  >>> device = simpleadb.AdbDevice('emulator-5554')
  >>> device.root()
  >>> device.reboot()

We can read all of the devices id's from the adb server. The ``adb.devices()``
command in the example below returns the list of ``AdbDevice`` objects of every
device connected to the adb.

.. code-block:: python

  >>> import simpleadb
  >>> adb = simpleadb.AdbServer()
  >>> devices = adb.devices()
  >>> devices
  ['emulator-5554', 'emulator-5555']
  >>> emulator = devices[0]
  >>> emulator.root()
  >>> emulator.reboot()

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

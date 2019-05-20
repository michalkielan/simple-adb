""" Interface for adb process"""
import subprocess
from . import adbcmds

class AdbProcess(object):
"""Adb process caller"""
  def __init__(self):
    self.__adb_path = adbcmds.ADB

  def call(self, args):
    """ Call process

      Args:
        Arguments
      Returns:
        0 if success, otherwise error code
    """
    cmd = ' '.join([
        self.__adb_path,
        args,
    ])
    return subprocess.call(cmd, shell=True)

  def check_call(self, args):
    """ Call process

      Args:
        Arguments
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        self.__adb_path,
        args,
    ])
    return subprocess.check_call(cmd, shell=True)

  def check_output(self, args):
    """ Call process

      Args:
        Arguments
      Returns:
        0 if success
      Raises:
        CalledProcessError: when failed
    """
    cmd = ' '.join([
        self.__adb_path,
        args,
    ])
    return subprocess.check_output(cmd, shell=True)

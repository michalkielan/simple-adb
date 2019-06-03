""" Interface for adb process"""
import subprocess
from . import adbcmds

class AdbProcess(object):
  """Adb process caller"""
  def __init__(self, path=adbcmds.ADB):
    self.__adb_path = path

  def call(self, args, **options):
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
    options.setdefault('shell', True)
    return subprocess.call(cmd, **options)

  def check_call(self, args, **options):
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
    options.setdefault('shell', True)
    return subprocess.check_call(cmd, **options)

  def check_output(self, args, **options):
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
    options.setdefault('shell', True)
    return subprocess.check_output(cmd, **options)

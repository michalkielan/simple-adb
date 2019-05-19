""" Interface for adb process"""
import subprocess
from . import adbcmds

def call(args):
  """ Call process

    Args:
      Arguments
    Returns:
      0 if success, otherwise error code
  """
  cmd = ' '.join([
      adbcmds.ADB,
      args,
  ])
  return subprocess.call(cmd, shell=True)

def check_call(args):
  """ Call process

    Args:
      Arguments
    Returns:
      0 if success
    Raises:
      CalledProcessError: when failed
  """
  cmd = ' '.join([
      adbcmds.ADB,
      args,
  ])
  return subprocess.check_call(cmd, shell=True)

def check_output(args):
  """ Call process

    Args:
      Arguments
    Returns:
      0 if success
    Raises:
      CalledProcessError: when failed
  """
  cmd = ' '.join([
      adbcmds.ADB,
      args,
  ])
  return subprocess.check_output(cmd, shell=True)

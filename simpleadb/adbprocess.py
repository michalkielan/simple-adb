""" Interface for adb process"""
import subprocess
from . import adbcmds # pylint: disable=relative-beyond-top-level


class AdbProcess(object): # pylint: disable=useless-object-inheritance
    """AdbProcess this class is used to call adb process

      Args:
        path (Optional[str]): adb path, default: 'adb'
      Returns:
        0 if success, otherwise error code
    """

    def __init__(self, path=adbcmds.ADB):
        self.__adb_path = path

    def call(self, args, **kwargs):
        """ Call process

          Args:
            args (str): Arguments
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec
          Returns:
            0 if success, otherwise error code
        """
        cmd = ' '.join([
            self.__adb_path,
            args,
        ])
        kwargs.setdefault('shell', True)
        return subprocess.call(cmd, **kwargs)

    def check_call(self, args, **kwargs):
        """ Call process

          Args:
            args (str): Arguments
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            self.__adb_path,
            args,
        ])
        kwargs.setdefault('shell', True)
        return subprocess.check_call(cmd, **kwargs)

    def check_output(self, args, **kwargs):
        """ Call process

          Args:
            args (str): Arguments
            **kwargs: Arbitrary keyword arguments
          Keyword Args:
            timeout (int): Timeout in sec
          Returns:
            0 if success
          Raises:
            CalledProcessError: when failed
        """
        cmd = ' '.join([
            self.__adb_path,
            args,
        ])
        kwargs.setdefault('shell', True)
        return subprocess.check_output(cmd, **kwargs)

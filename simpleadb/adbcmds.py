""" List of strings with adb commands """

ENV_SERVER_PORT = 'ANDROID_ADB_SERVER_PORT'
ENV_ADB_TRACE = 'ADB_TRACE'
ENV_ADB_VENDOR_KEYS = 'ADB_VENDOR_KEYS'
ENV_ANDROID_SERIAL = 'ANDROID_SERIAL'
ENV_ANDROID_LOG_TAGS = 'ANDROID_LOG_TAGS'

ADB = 'adb'
ROOT = 'root'
UNROOT = 'unroot'
REMOUNT = 'remount'
REBOOT = 'reboot'
INPUT_TAP = 'input tap'
SCREENCAP = 'screencap'
PM_GRANT = 'pm grant'
SETPROP = 'setprop'
GETPROP = 'getprop'
USB = 'usb'
SHELL = 'shell'
PULL = 'pull'
PUSH = 'push'
DISABLE_VERITY = 'disable-verity'
ENABLE_VERITY = 'enable-verity'
UNINSTALL = 'uninstall'
INSTALL = 'install'
FORWARD = 'forward'
DEVPATH = 'get-devpath'
DEVICES = 'devices'
GET_SERIALNO = 'get-serialno'
DISCONNECT = 'disconnect'
CONNECT = 'connect'
WAIT_FOR_DEVICE = 'wait-for-device'
KILL_SERVER = 'kill-server'
START_SERVER = 'start-server'
TCPIP = 'tcpip'
RM = 'rm'
GET_STATE = 'get-state'
VERSION = 'version'
LOGCAT = 'logcat'


def get_set_device(device_id):
    """ Set specific device to adb command

      Args:
        Device id
      Returns:
        String to set device id in adb command
    """
    return '-s ' + str(device_id)

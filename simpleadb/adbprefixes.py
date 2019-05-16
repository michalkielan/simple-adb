def get_env_server_port():
  return 'ANDROID_ADB_SERVER_PORT'

def get_env_adb_trace():
  return 'ADB_TRACE'

def get_env_adb_vendor_keys():
  return 'ADB_VENDOR_KEYS'

def get_env_android_serial():
  return 'ANDROID_SERIAL'

def get_env_android_log_tags():
  return 'ANDROID_LOG_TAGS'

def get_adb_prefix():
  return 'adb'

def get_root():
  return 'root'

def get_unroot():
  return 'unroot'

def get_remount():
  return 'remount'

def get_reboot():
  return 'reboot'

def get_input_tap():
  return 'input tap'

def get_pm_grant():
  return 'pm grant'

def get_usb():
  return 'usb'

def get_shell():
  return 'shell'

def get_pull():
  return 'pull'

def get_push():
  return 'push'

def get_uninstall():
  return 'uninstall'

def get_install():
  return 'install'

def get_forward():
  return 'forward'

def get_devpath():
  return 'get-devpath'

def get_devices():
  return 'devices'

def get_get_serialno():
  return 'get-serialno'

def get_disconnect():
  return 'disconnect'

def get_connect():
  return 'connect'

def get_wait_for_device():
  return 'wait-for-device'

def get_kill_server():
  return 'kill-server'

def get_start_server():
  return 'start-server'

def get_tcpip():
  return 'tcpip'

def get_get_state():
  return 'get-state'

def get_version():
  return 'version'

def get_set_device(device_id):
  return '-s ' + str(device_id)

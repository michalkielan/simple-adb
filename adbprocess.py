import subprocess

def get_adb_prefix():
  return 'adb '

def call(args):
  return subprocess.call([get_adb_prefix() + args], shell=True)

def check_call(args):
  return subprocess.check_call([get_adb_prefix() + args], shell=True)

def check_output(args):
  return subprocess.check_output(get_adb_prefix() + args, shell=True)

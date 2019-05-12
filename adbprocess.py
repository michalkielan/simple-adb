import subprocess
import adbprefixes

def call(args):
  cmd = ' '.join([
      adbprefixes.get_adb_prefix(),
      args,
  ])
  return subprocess.call(cmd, shell=True)

def check_call(args):
  cmd = ' '.join([
      adbprefixes.get_adb_prefix(),
      args,
  ])
  return subprocess.check_call(cmd, shell=True)

def check_output(args):
  cmd = ' '.join([
      adbprefixes.get_adb_prefix(),
      args,
  ])
  return subprocess.check_output(cmd, shell=True)

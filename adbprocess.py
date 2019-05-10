import subprocess

def call(cmd):
  return subprocess.call(['adb ', cmd])

def check_call(cmd):
  return subprocess.check_call(['adb', cmd])

def check_output(cmd):
  return subprocess.check_output('adb ' + cmd, shell=True)


import subprocess

def call(cmd):
  subprocess.call(['adb', cmd])

def check_output(cmd):
  return subprocess.check_output('adb ' + cmd, shell=True)


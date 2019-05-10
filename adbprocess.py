import subprocess

def call(args):
  return subprocess.call(['adb ' + args], shell=True)

def check_call(args):
  return subprocess.check_call(['adb ' + args], shell=True)

def check_output(args):
  return subprocess.check_output('adb ' + args, shell=True)


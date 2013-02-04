#!/usr/bin/python
import serial, getopt, textwrap, sys, threading, time
from ola.ClientWrapper import ClientWrapper

def HandleData(data):
    print(data)

def Usage():
    print textwrap.dedent("""
  Usage: ola_prz.py --universe <universe> --device <device>

  -h, --help                Display this help message and exit.
  -u, --universe <universe> Universe number.""")

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hu:d:', ['help', 'universe=', 'device='])
  except getopt.GetoptError, err:
    print str(err)
    Usage()
    sys.exit(2)

  universe = 1
  device = '/dev/ttyUSB0'
  for o, a in opts:
     if o in ('-h', '--help'):
          Usage()
          sys.exit()
     elif o in ('-u', '--universe'):
         universe = int(a)

  wrapper = ClientWrapper()
  client = wrapper.Client()
  client.RegisterUniverse(universe, client.REGISTER, HandleData)
  wrapper.Run()

if __name__ == '__main__':
    main()

#!/usr/bin/python
import serial, getopt, textwrap, sys, threading, time
from ola.ClientWrapper import ClientWrapper

def SerialThread(device):
    while globals()['running']:
        try:
            print('Connecting to '+device)
            port = serial.Serial(device, 1000000)

            while globals()['running']:
                if 'buffer' in globals():
                    packet = bytes()
                    buf = globals()['buffer']
                    length = len(buf)

                    packet += chr(0xaa)
                    packet += chr((length>>8)&0xff)
                    packet += chr(length&0xff)
                    for x in xrange(length):
                        packet += chr(buf[x])

                    #print(ord(packet[3]))
                    port.write(packet)

                time.sleep(1.0/100)

            port.close()
        except serial.SerialException:
            time.sleep(1)

def HandleData(data):
    if 'buffer' in globals():
        lastSize = len(globals()['buffer'])
    else:
        lastSize = 0
    size = 0
    target = []
    temp = []
    for x in data:
        temp += [x]
        if x != 0 or size<lastSize:
            target += temp
            temp = []
        size += 1

    globals()['buffer'] = target

def Usage():
    print textwrap.dedent("""
  Usage: ola_prz.py --universe <universe> --device <device>

  -h, --help                Display this help message and exit.
  -d, --device              The serial device to use
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
     elif o in ('-d', '--device'):
         device = str(a)

  globals()['running'] = True

  serialThread = threading.Thread(None, SerialThread, None, (device,))
  serialThread.start()

  while True:
      try:
          print('Running OLA client')
          wrapper = ClientWrapper()
          client = wrapper.Client()
          client.RegisterUniverse(universe, client.REGISTER, HandleData)
          wrapper.Run()
      except KeyboardInterrupt:
          raise
      except:
          time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating...')
        globals()['running'] = False

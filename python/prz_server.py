#!/usr/bin/python
import serial, getopt, textwrap, sys, threading, time, socket

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
                    #print('Sending '+str(length))
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

def ClientLoop(s):
    dead = False
    state = 0
    l = 0
    data = []
    while not dead:
        c = s.recv(1024)
        if not c:
            dead = True
        else:
            for x in xrange(len(c)):
                h = c[x]
                if state == 3:
                    data += [ord(h)]
                    l = l-1
                    if l <= 0:
                        HandleData(data)
                        state = 0
                else:
                    if state == 2:
                        l |= ord(h)
                        print('Len=' + str(l))
                        data = []
                        state = 3
                    if state == 1:
                        l = ord(h)<<8
                        state = 2
                    if state == 0 and h == b'\xaa':
                        state = 1                    

def ServerLoop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 2525))
    s.listen(10)
    print('Entering server loop')
    while True:
        (c, a) = s.accept()
        ClientLoop(c)

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
  device = '/dev/ttyUSB1'
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
          print('Running server')
          ServerLoop()
      except KeyboardInterrupt:
          raise
      #except:
      #    time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminating...')
        globals()['running'] = False

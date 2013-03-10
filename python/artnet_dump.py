#!/usr/bin/python

import select, socket, time

target = ('192.168.0.22', 2525)

port = 6454  # where do you expect to get a msg?
bufferSize = 1024 # whatever you need

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('192.168.0.255', port))
s.setblocking(0)

print('Listening...')
start = time.time()

while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize) 
    arr = []
    for x in xrange(len(msg)):
        arr += [ord(msg[x])]
    print(str(time.time()-start)+': Packet for universe = '+str(ord(msg[14]))+' ...')

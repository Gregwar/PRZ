#!/usr/bin/python

import select, socket 

target = ('192.168.0.22', 2525)

port = 6454  # where do you expect to get a msg?
bufferSize = 1024 # whatever you need

o = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
o.bind(target)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('192.168.0.255', port))
s.setblocking(0)

print('Listening...')

while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize) 
    if ord(msg[14]) == 1:
        o.send(msg)

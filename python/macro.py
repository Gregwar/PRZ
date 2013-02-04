#!/usr/bin/python

from osc import OSC
from subprocess import call
import threading
import time

# Mots
words = [
    ["push1", "hello"],
    ["push2", "bonjour"]
]
 
#------OSC Server-------------------------------------#
receive_address = '0.0.0.0', 8000
 
# OSC Server. there are three different types of server. 
s = OSC.ThreadingOSCServer(receive_address)
 
# this registers a 'default' handler (for unmatched messages)
s.addDefaultHandlers()
 
# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    for couple in words:
        push, word = couple
        if addr.endswith(push) and stuff[0]==1.0:
            print(addr)
            call(["osascript", "-e", "tell application \"System Events\" to keystroke \""+word+"\""])

 
s.addMsgHandler('default', printing_handler)
 
def main():
    # Start OSCServer
    print('Starting OSCServer')
    st = threading.Thread(target=s.serve_forever)
    st.start()

try:
    main()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.running = False
    print("Stop!")


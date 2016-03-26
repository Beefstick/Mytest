#!/usr/bin/python           # This is client connecting to remote/local ip

import socket               # Import socket module
import sys                  # for exit
import time


#------------------------ socket descriptor ----------------------------
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

# "Every IP packet contains a TTL,
# initialized to some default value and decremented by each router that handles the packet.
# When the TTL reaches 0, the packet is discarded.
# By setting the TTL, we limit the number of hops a multicast packet can traverse from the sender.
# The TTL may also be set for broadcast;
# however, since routers generally do not forward broadcast packets, it usually has no effect.
try:
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
except socket.error, msg:
    print 'Failed to set socket option for IP_MULTICAST_TTL. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'

#------------------------ server IP ----------------------------
remote_ip = "224.0.0.0" # class D: 224.0.0.0 ~ 239.255.255.255
port = 12345                # Reserve a port for your service.

#------------------------ send data ----------------------------

while True:
    message = "This is a periodic multicast message."
    try :
        #Set the whole string
        s.sendto(message, (remote_ip, port))
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
    print 'Message send successfully'
    time.sleep(2)
# should never get here
raw_input('Press <ENTER> to close program')
s.close

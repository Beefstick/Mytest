import socket
import sys

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

nick = raw_input("Please choose a nick name: ")
sending = True
joined = nick + " has joined the chat."
sock.sendto(joined.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
while (sending):
    sendmsg = raw_input('send what message? \n')
    
    if sendmsg == '/exit':
        exiting = nick + " has now left the chat."
        sock.sendto(exiting.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
        print("leaving chat...")
        break
    elif sendmsg.startswith('/nick ') == True:
        nickchange = nick + " is now known as: " + sendmsg.split(sep=None, maxsplit=1)[1]
        sock.sendto(nickchange.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
        nick = sendmsg.split(sep=None, maxsplit=1)[1]
    elif sendmsg.startswith('/') == True:
        print("Command not recognized")
    else:
        parsedmsg = nick + ": " + sendmsg
        sock.sendto(parsedmsg.encode(encoding='utf_8', errors='strict'), (MCAST_GRP, MCAST_PORT))
print("You have left the chat.")

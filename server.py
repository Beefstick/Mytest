import csv
import sys
import socket
import select
import os

HOST = '' 
SOCKET_LIST = []
STUDENT_CLIENT = []
TA_CLIENT = []
RECV_BUFFER = 4096 
PORT = 9009

def server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    writable_sockets = []
    
    files = os.listdir(os.curdir)

    SOCKET_LIST.append(server_socket)
 
    print "Instructor grade server started on port " + str(PORT)

    flag = False
    send_file_size = False
 
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,writable_sockets,[],0)
        
	for sock in ready_to_write:
		if send_file_size == True:
			sock.sendall(str(file_size))
			send_file_size = False
			flag = True
		elif flag == True and file_size != 0:	
			buf = file_to_send.read(RECV_BUFFER)
			sock.sendall(buf)
			file_size -= len(buf)

			if file_size <= 0:
				file_to_send.close()
				flag = False
				ready_to_write = []
				print "Done sending"

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
			if (data == "Student"):
				STUDENT_CLIENT.append(sockfd) 
                		broadcast(server_socket, sockfd, "[%s:%s] (Student client) joined session\n" % addr)
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                   	print data
			words = str.split(data)
			if (words[0] == "LIST"):
				files = os.listdir(os.curdir)
				sock.sendall(files[1])
			elif (words[0] == "READ" and len(words) > 1):
				files = os.listdir(os.curdir)
				for f in files:
					if (f == words[1]):
						print "Found file\n"
						file_to_transfer = f
						file_size = os.path.getsize(os.path.realpath(words[1]))  
						print file_size
						writable_sockets = [sock]
						file_to_send = open(f, 'rb') #Open in binary, r = read
						send_file_size = True
						#buf = file_to_send.read(RECV_BUFFER)
						#while (buf):
						#	print "Hello"
						#	sock.send(buf)
						#	buf = file_to_send.read(RECV_BUFFER)
						#f.close()
						#print "Done sending"
				
		    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(server())  

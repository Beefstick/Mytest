
import threading
import SocketServer
import os
import sys
import socket
import time

mypath = 'C:\\Users\\Jeff\\Desktop\\Class Lectures\\Level 4 Term 2\\Comp Eng 4DN4\\lab3\\default - Copy\\A\\'
BUFF = 1024

host = "localhost 3000"
known_hosts = ['localhost 3001']
default_known_hosts = ['localhost 3001']
found_list = []
found_hosts = []


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        cur_thread = threading.current_thread()  # identify current thread

        thread_name = cur_thread.name   # get thread-number in python

        #print '\nServer Thread %s receives request ' % thread_name

        while 1:
            data = self.request.recv(BUFF)
            if "1"==data.rstrip():
                self.listing(thread_name)
                break
            if "2"==data.rstrip():
                self.read_f(thread_name)
                break
            if "3"==data.rstrip():
                self.search(thread_name)
                break
            if "4"==data.rstrip():
                self.found_file(thread_name)
                break
            if "5"==data.rstrip():
                self.discover(thread_name)
                break
            if "6"==data.rstrip():
                self.found_host(thread_name)
                break

        #print '\nServer Thread %s terminating' % thread_name



    def listing(self,thread_name):
        path = mypath
        myString = '\n'
        for root, dirs, files in os.walk( path ):
            for name in files:
                #parent = root.split(path)
                #myString = myString + os.path.join(parent[1],name) + '\n' #gives subfolder(s) + filename
                myString = myString + name + '\n'
        myString="=======List======\n"+myString+"\n================="
        data=str(sys.getsizeof(myString))
        self.request.send(data)
        self.request.send(myString)

        self.request.close()

    def read_f(self,thread_name):
        found = False
        data = self.request.recv(BUFF)
        for root, dirs, files in os.walk( mypath ):
            for name in files:
                if name == str(data):
                    parent = root.split(mypath)
                    file = os.path.join(parent[1],name)
                    found = True
        if found == True:
            size= os.path.getsize(mypath+file)
            self.request.sendall(str(size))
            f=open(mypath+file,'rb')
            data = f.read()
            f.close()
            self.request.send(data)
        else:
            self.request.sendall('None')

        self.request.close()


    def search(self,thread_name):
        self.request.send('ack')
        TTL = int(self.request.recv(BUFF))
        self.request.send('ack')
        file = self.request.recv(BUFF)
        self.request.send('ack')
        raddress = str(self.request.recv(BUFF))

        if TTL >= 0:

            path = mypath
            found = False
            for root, dirs, files in os.walk( path ):
                for name in files:
                    if name == file:
                        found = True

            if found == True:

                names = raddress.split(" ")
                rhost = names[0]
                rport = int(names[1])
                server_address = ((rhost,rport))
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_address)

                    #call found file on querying peer
                    sock.send('4')
                    ack = sock.recv(1024)
                    sock.send(host)

                    sock.close()
                except:
                    a=0

        if TTL != 0:
            for entry in known_hosts:
                if entry != raddress:
                    names = entry.split(" ")
                    rhost = names[0]
                    rport = int(names[1])
                    server_address = ((rhost,rport))

                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect(server_address)

                        #call search on known peers
                        sock.send('3')
                        ack = sock.recv(1024)
                        mTTL = TTL-1
                        sock.send(str(mTTL))
                        ack = sock.recv(1024)
                        sock.send(file)
                        ack = sock.recv(1024)
                        sock.send(raddress)

                        sock.close()
                    except:
                        a=0

        self.request.close()

    def found_file(self,thread_name):
        self.request.send('ack')
        rhost = str(self.request.recv(BUFF))

        found_list.append(rhost.rstrip())

    def discover(self,thread_name):
        self.request.send('ack')
        TTL = int(self.request.recv(BUFF))
        self.request.send('ack')
        raddress = str(self.request.recv(BUFF))

        if TTL >= 0:

            names = raddress.split(" ")
            rhost = names[0]
            rport = int(names[1])
            server_address = ((rhost,rport))

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(server_address)

                #call found host on querying host
                sock.send('6')
                ack = sock.recv(1024)
                sock.send(host)

                sock.close()
            except:
                a=0

        if TTL != 0:
            for entry in known_hosts:
                if entry != raddress:
                    names = entry.split(" ")
                    rhost = names[0]
                    rport = int(names[1])
                    server_address = ((rhost,rport))

                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect(server_address)

                        #call discover on knownhosts
                        sock.send('5')
                        ack = sock.recv(1024)
                        mTTL = TTL-1
                        sock.send(str(mTTL))
                        ack = sock.recv(1024)
                        sock.send(raddress)

                        sock.close()
                    except:
                        a=0

        self.request.close()


    def found_host(self,thread_name):
        self.request.send('ack')
        rhost = str(self.request.recv(BUFF))

        found_hosts.append(rhost.rstrip())

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def cleanlist(hostlist):
    a = list(set(hostlist))

    cleanlist = [x for x in a if x != host]

    #print cleanlist
    return cleanlist

if __name__ == "__main__":
    names = host.split(' ')
    HOST = names[0]
    PORT = int(names[1])

    print "\nStart Threaded-Server on PORT %s " % PORT

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()
    print "Main Server using thread %s " % server_thread.name

    while 1:
        print ("""
        1.LISTL
        2.LISTR
        3.SEARCH
        4.DISCOVER
        5.RESET
        6.GET
        7.QUIT
        """)
        msg = raw_input("Please enter CMD (1-7): ")
        if msg == "1":

            path = mypath
            myString = '\n'
            for root, dirs, files in os.walk( path ):
                for name in files:
                    myString = myString + name + '\n'
            myString="=======List======\n"+myString+"\n================="
            print myString

        if msg == "2":
            rhost = raw_input("Please enter IP or localhost: ")
            rport = int(raw_input("Please enter port: "))
            server_address = ((rhost, rport))
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(server_address)

                sock.sendall("1")
                size=sock.recv(1024)
                amount_expected=int(size)
                amount_received = 0

                print '\n'
                while amount_received< amount_expected:
                    data=sock.recv(1024)
                    amount_received += sys.getsizeof(data)
                    print data
                print '\n'
            except:
                print '\nConnection Error for ' + rhost + " " + str(rport) + '\n'

        elif msg == "3":
            TTL = int(raw_input("Please enter TTL: "))
            file = raw_input("Please enter filename: ")

            if TTL >= 1:
                found_list = []
                for entry in known_hosts:
                    names = entry.split(' ')
                    rhost = names[0]
                    rport = int(names[1])
                    server_address = ((rhost, rport))
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect(server_address)

                        sock.send('3')
                        ack = sock.recv(1024)
                        mTTL = TTL - 1
                        sock.send(str(mTTL))
                        ack = sock.recv(1024)
                        sock.send(file)
                        ack = sock.recv(1024)
                        sock.send(host)

                        sock.close()
                    except:
                        print '\nConnection Error for ' + rhost + " " + str(rport) + '\n'

                time.sleep(1)

                if found_list == []:
                    print "File not found"
                else:
                    hosts = cleanlist(found_list)
                    for entry in hosts:
                        print "File found at " + entry
            else:
                print "\nEnter a TTL greater than 0\n"

        elif msg == "4":
            TTL = int(raw_input("Please enter TTL: "))

            if TTL >= 1:
                found_hosts = []
                for entry in known_hosts:
                    names = entry.split(' ')
                    rhost = names[0]
                    rport = int(names[1])
                    server_address = ((rhost, rport))
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect(server_address)

                        sock.send('5')
                        ack = sock.recv(1024)
                        mTTL = TTL - 1
                        sock.send(str(mTTL))
                        ack = sock.recv(1024)
                        sock.send(host)

                        sock.close()
                    except:
                        print '\nConnection Error for ' + rhost + " " + str(rport) + '\n'

                time.sleep(1)

                hosts = cleanlist(found_hosts)
                print "\nNew Peers:"
                print list(set(hosts) - set(known_hosts))
                print "\nAll Peers:"
                print hosts

                known_hosts = hosts[:]
            else:
                print "\nEnter a TTL greater than 0\n"

        elif msg == "5":

                known_hosts = default_known_hosts[:]
                print '\nReset known peers\n'

        elif msg == "6":

                rhost = raw_input("Please enter IP or localhost: ")
                rport = int(raw_input("Please enter port: "))
                server_address = ((rhost, rport))
                # Create a TCP/IP socket
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_address)

                    sock.sendall("2")
                    msg2 = raw_input("Enter file name with extension to download: ")
                    sock.sendall(msg2)
                    data = None
                    size=sock.recv(1024)
                    #print size
                    if size != 'None':
                        amount_expected=int(size)
                        amount_received = 0
                        with open(mypath+str(msg2), 'wb+') as file_to_write:
                            while amount_received< amount_expected:
                                data=sock.recv(1024)
                                if data:
                                    amount_received += len(data)
                                    file_to_write.write(data)
                                else:
                                    print "\nbroken pipe\n"
                                    os.remove(mypath+str(msg2))
                                    break
                        print "\nDownload Complete\n"
                    else:
                        print "\nFile not found\n"
                except:
                    print '\nConnection Error for ' + rhost + " " + str(rport) + '\n'



        elif msg == "7":
            print '\nQuit\n'
            break
        else:

            print "\nInvalid Option\n"
            continue

    print''


    print '\nMain server thread shutting down the server and terminating'
    server.shutdown()



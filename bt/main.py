#!/usr/bin/python

from btfiler import *
import threading

def main():
   btpeer = FilerPeer(10, 9998)
   #btpeer.buildpeers('localhost', 9998, 5)
   #btpeer.addpeer(666, 'localhost', 9999)   

   #t = threading.Thread(target = btpeer.mainloop, args = [] )
   #t.start()

   #conn = BTPeerConnection(666, 'localhost', 9999)

   #btpeer.startstabilizer(btpeer.checklivepeers, 3)
   btpeer.mainloop()

main()


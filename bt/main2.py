#!/usr/bin/python

from btfiler import *
import threading

def main():
   btpeer = FilerPeer(10, 9999)
   #btpeer.buildpeers('localhost', 9998, 5)
   #btpeer.addpeer(667, 'localhost', 9998)   

   #t = threading.Thread(target = btpeer.mainloop, args = [] )
   #t.start()

   conn = BTPeerConnection(667, 'localhost', 9998)

   btpeer.mainloop()

   #btpeer.startstabilizer(btpeer.checklivepeers, 3)

main()


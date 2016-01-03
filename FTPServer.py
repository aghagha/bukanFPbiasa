import socket
import os
import threading
import select
import sys
import os
import time

currdir=os.path.abspath('.')
local_ip='localhost'
class Server:
	def __init__(self):
		self.host = localhost
		self.port = 5000
		self.size = 1024
		self.server = None
		self.threads = []

	def open_socket(self): #function to open server socket
	 	self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5) 

    def run(self):
    	self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

        class Client(threading.Thread):
		    def __init__(self,(conn,addr)):
		        self.conn=conn
		        self.addr=addr
		        self.basewd=currdir
		        self.cwd=self.basewd
		        self.rest=False
		        self.pasv_mode=False
		        self.passwd=''
		        threading.Thread.__init__(self)

    	

if __name__ == '__main__':
	# run server class
	s = server()
	s.run


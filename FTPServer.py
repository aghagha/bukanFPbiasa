import socket
import os
import threading
import select
import sys

class Server:
	def __init__(self):
		self.host = 
		self.port = 
		self.size = 1024
		self.server = None
		self.threads = []

	def open_socket(self): #function to open server socket
	 	self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5) 

    def run():
    	

if __name__ == '__main__':
	# run server class
	s = server()
	s.run


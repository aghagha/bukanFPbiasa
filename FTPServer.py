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
                    c = FTPthread(self.server.accept())
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

class FTPthread(threading.Thread):
    #init value untuk setiap thread
    def __init__(self,(conn,addr)):
        self.conn=conn
        self.addr=addr
        self.basewd=currdir
        self.cwd=self.basewd
        self.rest=False
        self.pasv_mode=False
        self.passwd=''
        self.running= True
        threading.Thread.__init__(self)

    def run(self):
        self.conn.send('220 Welcome\r\n')
        while self.running :
            cmd = self.conn.recv(1024)
            if not cmd: break
            else:
                print 'Received:',cmd
                func = getattr(self,cmd[:4].strip().upper())
                func(cmd)

        self.conn.close()
    
    # get User and check whether user is on user.txt or not , if exist set password for next command
    def USER(self,cmd):
        with open('user.txt','r') as search:
            for line in search:
                if cmd[5:-2] in line:
                    user = line.split('\t')[0]
                    self.passwd = line.split('\t')[1].split('\n')[0]
                    break

        self.conn.send('331 User ' +user + 'OK.Password Required\r\n')
    # compare input PASS and in user.txt
    def PASS(self):
        if self.passwd != cmd[5:-2]:
            self.conn.send('530 Login Authentication Failed.\r\n')
            self.running = False
        else
            self.conn.send('230 Login successfull\r\n')
			
	def HELP(self, cmd):
        self.conn.send('214-The following commands are recognized.\r\nCWD DELE HELP LIST MKD PASS PWD QUIT RETR RMD RNTO RNFR STOR USER\r\n')
        self.conm.send('214 Help OK.')
		
    def Quit(self):
        self.conn.send('221 Goodbye\r\n')
        self.running = False

    def PWD(self,cmd):
        cwd=os.path.relpath(self.cwd,self.basewd)
        if cwd=='.':
            cwd='/'
        else:
            cwd='/'+cwd
        self.conn.send('257 \"%s\"\r\n' % cwd)

    def CWD(self,cmd):
        chwd=cmd[4:-2]
        if chwd=='/':
            self.cwd=self.basewd
        elif chwd[0]=='/':
            self.cwd=os.path.join(self.basewd,chwd[1:])
        else:
            self.cwd=os.path.join(self.cwd,chwd)
        self.conn.send('250 OK.\r\n')

    def MKD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        os.mkdir(dn)
        self.conn.send('257 Directory created.\r\n')

    def RMD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        if allow_delete:
            os.rmdir(dn)
            self.conn.send('250 Directory deleted.\r\n')
        else:
            self.conn.send('450 Not allowed.\r\n')

if __name__ == '__main__':
	# run server class
	s = server()
	s.run


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
		self.host = local_ip
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
        self.auth = 0
        threading.Thread.__init__(self)

    def run(self):
        self.conn.send('220 Welcome\r\n')
        while self.running :
            cmd = self.conn.recv(1024)
            if not cmd: break
            else:
                if cmd[:4] == 'USER':
                    func=getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                    self.auth= 1
                elif cmd[:4] =='PASS':
                    func=getattr(self,cmd[:4].strip().upper())
                    func(cmd)
                    self.auth = 2
                elif self.auth == 2:
                    print 'Recieved:',cmd
                    try:
                        func=getattr(self,cmd[:4].strip().upper())
                        func(cmd)
                    except Exception,e:
                        print 'ERROR:',e
                        #traceback.print_exc()
                        self.conn.send('500 Sorry.\r\n')
                else:
                    self.conn.send('Error login required\r\n')

        #self.conn.close()
    
    # get User and check whether user is on user.txt or not , if exist set password for next command
    def USER(self,cmd):
        with open('user.txt','r') as search:
            for line in search:
                if cmd[5:-2] in line:
                    user = line.split('\t')[0]
                    self.passwd = line.split('\t')[1].split('\n')[0]
                    break

        self.conn.send('331 Please specify the password\r\n')
    # compare input PASS and in user.txt
    def PASS(self,cmd):
        if self.passwd != cmd[5:-2]:
            self.conn.send('530 Login authentication failed.\r\n')
            self.running = False
        else:
            self.conn.send('230 Login successfull\r\n')
			
	def HELP(self, cmd):
        self.conn.send('214-The following commands are recognized.\r\nCWD DELE HELP LIST MKD PASS PWD QUIT RETR RMD RNTO RNFR STOR USER\r\n')
        self.conm.send('214 Help OK.')
		
    def QUIT(self):
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

    def LIST(self,cmd):
        self.conn.send('150 Here comes the directory listing.\r\n')
        print 'list:', self.cwd
        for t in os.listdir(self.cwd):
            print os.path.join(self.cwd,t)
            k=self.toListItem(os.path.join(self.cmd,t))
            self.conn.send(k+'\r\n')
        self.conn.send('226 Directory send OK.\r\n')
    
    def toListItem(self,fn):
        st=os.stat(fn)
        fullmode='rwxrwxrwx'
        mode=''
        for i in range(9):
            mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
        d=(os.path.isdir(fn)) and 'd' or '-'
        ftime=time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
        return d+mode+' 1 user group '+str(st.st_size)+ftime+os.path.basename(fn)

    def MKD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
        os.mkdir(dn)
        self.conn.send('257 Directory created.\r\n')

    def RMD(self,cmd):
        dn=os.path.join(self.cwd,cmd[4:-2])
            os.rmdir(dn)
            self.conn.send('250 Directory deleted.\r\n')
    
    def DELE(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        if mswindows:
            terminalcmd = 'RMDIR '+fn + " /s /q"
        else:
            terminalcmd = 'rmd -rf '+cmd[5:-2]
        result = getstatusoutput(terminalcmd)
        #os.remove(fn)
        self.conn.send('250 File deleted.\r\n')

    def RETR(self,cmd):
        fn=os.path.join(self.cwd,cmd[5:-2])
        print 'Downloading', fn

        fi = open (fn, 'rb')
        self.conn.send('150 Opeing data connection.\r\n')
        if self.rest:
            fi.seek(self.pos)
            self.rest = False
        data = fi.read(1024)
        while data:
            data = fi.read(1024)
        fi.close()
        self.conn.send('226 Transfer complete.\r\n')

if __name__ == '__main__':
	# run server class
	s = server()
	s.run


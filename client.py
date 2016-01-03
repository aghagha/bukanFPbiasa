import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect (('127.0.0.1', 5000))

if s.connect:
	print "telah terhubung dengan server"


	print "Selamat datang di FTP CLIENT\r\n"
	print "silahkan masukan perintah FTP anda\r\n"
	data = s.recv(1024)
	print data

	
	while(1):
		command=raw_input("masukan perintah anda>>  ")
		if "LIST" in command:
			s.send(command+'\r\n')
			msg=s.recv(1024)
			print msg

		elif "QUIT" in command:
			s.send(command+'\r\n')
			msg=s.recv(1024)
			print msg
			#break 

		elif "MKD" in command:
			foldername=raw_input("Masukan nama folder yang ingin dibuat >> ")
			cmd=('MKD '+foldername+'\r\n')
			s.send(cmd)
			msg=s.recv(1024)
			print msg

		elif "RMD"in command:
			foldername=raw_input("Masukan nama folder yang ingin dihapus >> ")
			cmd=('RMD '+foldername+'\r\n')
			s.send(cmd)
			msg=s.recv(1024)
			print msg

		elif "RNFR" in command:
			filename=raw_input("masukan nama file yang ingin dirubah>> ")
			
			cmd='RNFR '+filename+'\r\n'
			new=raw_input("masukan nama file yang baru>> ")
			command='RNTO '+new+'\r\n'
			s.send(cmd)
			msg1=s.recv(1024)
			s.send(command)
			msg=s.recv(1024)
			print msg1
			print msg

		elif "DELE" in command:
			filename=raw_input("masukan nama file yang ingin dirubah>> ")
			cmd='DELE '+filename+'\r\n'
			s.send(cmd)
			msg=s.recv(1024)
			print msg

		elif "PWD" in command:
			cmd='PWD\r\n'
			s.send(cmd)
			msg=s.recv(1024)
			print msg

		elif "CWD" in command:
			directory=raw_input("masukan nama directory yang ingin dituju>> ")
			cmd="CWD "+directory+'\r\n'
			s.send(cmd)
			msg=s.recv(1024)
			print msg

		elif "HELP" in command:
			s.send("HELP\r\n")
			msg=s.recv(1024)
			print msg

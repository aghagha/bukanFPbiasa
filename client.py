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
		if "USER" in command:
			username=raw_input("masukan username>> ")
			s.send(command+' '+username+'\r\n')
			msg=s.recv(1024)
			print msg

			password=raw_input("masukan password>> ")
			s.send('PASS '+password+'\r\n')
			msg=s.recv(1024)
			print msg

		# if "PASS" in command:
		# 	password=raw_input("masukan password>> ")
		# 	s.send(command+' '+password+'\r\n')
		# 	msg=s.recv(1024)
		# 	print msg

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

		elif "RETR" in command:
			filename=raw_input("masukkan nama file yang ingin diunduh>> ")
			s.send(command+' '+filename+'\r\n')
			msg=s.recv(1024)
			print msg
			
			f=open(filename,'wb')

			size = int(s.recv(16))
			diterima = ''
			while size > len(diterima):
				data = s.recv(1024)
				if '\r\n\r\n' in data:
					msg = data.split('\r\n\r\n')[1]
					print msg
					dataakhir = data.split('\r\n\r\n')[0]
					diterima += dataakhir
					f.write(data)
				if not data:
					break
				diterima += data
				f.write(data)

		elif "STOR" in command:
			fn=raw_input("masukan nama file yang ingin diunggah>> ")
			s.send(command+' '+fn+'\r\n')
			# msg=s.recv(4096)
			# print msg
			#msg = s.recv(1024)
			#print msg
			with open(fn,'rb') as f:
				data=f.read()
			s.sendall('%16d' % len(data))
			s.sendall(data)

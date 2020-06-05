""" Simple file system, user side, upload/download files 
"""

import os
import socket
import time

def fileUpload(fileName, sock):
	if os.path.isfile(fileName):
		sock.send(str("size" + str(os.path.getsize(fileName))).encode())
		with open(fileName, 'rb') as f:
			dataToSend = f.read(1024)
			sock.send(dataToSend)
			while dataToSend != '':
				dataToSend = f.read(1024)
				sock.send(dataToSend)
	else:
		raise Exception("Error, file does NOT exist")

	sock.close()

def fileDownload(sock):

	fileSize = int(sock.recv(1024)[4:].decode())
	fileName = sock.recv(1024).decode()


	with open(fileName, 'wb') as f:
		data = sock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = sock.recv(1024)
			totalRecv += len(data)
			f.write(data)



def Main():
	
	host = '18.166.56.143'
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.settimeout(50)
	s.connect((host,port))
	
	userRequest = input('upload/download/quit?')
	if userRequest == 'upload':
		fileName = input('name of file')
		s.send(str("upload" + fileName).encode())
		fileUpload(fileName, s)

	elif userRequest == 'download':
		s.send(str("download").encode())
		fileDownload(s)
	elif userRequest == 'quit':
		exit()

	s.close()
		
if __name__ == "__main__":
	Main()


	

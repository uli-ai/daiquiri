""" Simple file system, user side, upload/download files 
"""

import os
import socket
import time

def fileUpload(fileName, sock):
	if os.path.isfile(fileName):
		sock.send("size" + str(os.path.getsize(fileName)))
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

	fileSize = int(sock.recv(1024)[4:])
	fileName = sock.recv(1024)


	with open(fileName, 'wb') as f:
		data = sock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = sock.recv(1024)
			totalRecv += len(data)
			f.write(data)



def Main():
	
	host = '18.163.180.86'
	port = 5555
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(20)
	s.connect((host, port))
	userRequest = raw_input('upload/download/quit?')
	if userRequest == 'upload':
		fileName = raw_input('name of file')
		s.send("upload" + fileName)
		fileUpload(fileName, s)

	elif userRequest == 'download':
		s.send("download")
		fileDownload(s)
	elif userRequest == 'quit':
		exit()

	s.close()
		
if __name__ == "__main__":
	Main()


	

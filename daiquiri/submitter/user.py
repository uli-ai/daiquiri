""" Simple file system, user side, upload/download files 
"""

import os
import socket
import time

def fileUpload(fileName, sock):
	if os.path.isfile(fileName):
		sock.send("size" + str(os.path.getsize(fileName)))
		with open(fileName, rb) as f:
			dataToSend = f.read(1024)
			sock.send(dataToSend)
			while dataToSend != '':
				dataToSend = f.read(1024)
				sock.send(dataToSend)
	else:
		raise Exception("Error, file does NOT exist")

	sock.close()

def fileRecv(sock):
	data = sock.recv(1024)
	fielSize = int(data[4:])
	fileName = sock.recv(1024)
	with open(fileName, 'wb') as f:
		data = sock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = s.recv(1024)
			totalRecv += len(data)
			f.write(data)



def Main():
	
	host = '127.0.0.1'
	port = 5000
	s = socket.socket()
	s.connect(host, port)

	if raw_input('upload/download/quit?') == 'upload':
		fileName = raw_input('name of file')
		s.send("upload" + fileName)
		fileUpload(filename, s)
	elif raw_input('upload/download/quit?') == 'download':
		s.send("download")
		fileRecv(s)
	elif raw_input('upload/download/quit?') == 'quit':
		break

	s.close()
		
if __name__ == "__main__":
	Main()


	
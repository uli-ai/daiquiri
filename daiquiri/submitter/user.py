""" Upload files from the client side 
"""

import os
import socket
import time

def fileUpload(filePath, sock):
	if os.path.isfile(filePath):
		sock.send("size" + str(os.path.getsize(filePath)))
		with open(filePath, rb) as f:
			dataToSend = f.read(1024)
			sock.send(dataToSend)
			while dataToSend != '':
				dataToSend = f.read(1024)
				sock.send(dataToSend)
	else:
		raise Exception("Error, file does NOT exist")

	sock.close()


def Main():
	
	host = '127.0.0.1'
	port = 5000
	s = socket.socket()
	s.connect(host, port)
	while True:
		if raw_input('upload a file? y/n') == 'n':
			break
		filename = raw_input('name of file')
		s.send(filename)
		fileUpload(filename, s)
	s.close()
		
if __name__ == "__main__":
	Main()


	
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
	
	host1 = '18.163.180.86'
	host2 = '172.31.37.134'
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(50)
	try:
		s.connect((host1,port))
		print("connected to host 1 addr")
	except:
		s.connect((host2,port))
		print("connected to host 2 addr")
	userRequest = input('upload/download/quit?')
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


	

""" A simple file system from the server side which takes cares 
of user/submitter's request of submitting training data or 
downloading a trained model/predicted result
"""

import os
import socket

def fileRecv(sock, addr, name):
	# if not os.path.exists("/" + str(addr)):
	# 	os.makedirs("/" + str(addr) + "/data")
	# 	os.makedirs("/" + str(addr) + "/result")
	# os.chdir("/" + str(addr) + "/data")
	fileSize = sock.recv(1024)[4:]
	with open(name, 'wb') as f:
		data = sock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = sock.recv(1024)
			
			totalRecv += len(data)
			f.write(data)
	

def fileRetriv(sock, addr):
	if not os.path.isdir("/home/" + addr):
		raise Exception("Result Not Exist")
	sock.send("size" + str(os.path.getsize(fileName)))
	sock.send(os.listdir)
	with open(fileName, rb) as f:
		dataToSend = f.read(1024)
		sock.send(dataToSend)
		while dataToSend != '':
			dataToSend = f.read(1024)
			sock.send(dataToSend)
	sock.close()

def Main():
	host = '127.0.0.1'
	port = 5000
	s = socket.socket()
	s.bind((host,port))
	s.listen(5)
	print("server started")

	while True:
		c, addr = s.accept()
		print('connected to ip {}'.format(addr))
		data = c.recv(1024)
		# listen to user's request
		if data[:2] == "up":
			fname = data[6:]
			fileRecv(c, addr, fname)
		elif data[:2] == "do":
			fileRetriv(c, addr)

if __name__ == '__main__':
	Main()
		
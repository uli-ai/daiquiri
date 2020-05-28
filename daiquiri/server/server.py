""" A simple file system from the server side which takes cares 
of user/submitter's request of submitting training data or 
downloading a trained model/predicted result
"""

import os
import socket

def fileRecv(sock, addr, name):
	if not os.path.exist("/home/" + addr):
		os.makedirs("/home/" + addr + "data")
		os.makedirs("/home/" + addr + "result")

	fileSize = sock.recv(1024)[4:]
	with open(name, wb) as f:
		data = s.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < filesize:
			data = s.recv(1024)
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

	while True:
		c, addr = s.accept
		print('connected to ip {}'.format(addr))
	    data = s.recv(1024)
	    if data[:2] == "up":
	    	fname = data[6:]
			fileRecv(s, addr, fname)
		elif data[:2] == "do":
			fileRetriv(s, addr)

if __name__ == '__main':
	Main()
		
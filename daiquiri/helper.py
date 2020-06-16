"""Daiquiri helper functions."""
import os
import tqdm
import socket


def fileSend(conn, fileName):
	"""Function used for sending files. 
	   Requires: valiad file name and path/route.
	   			 established socket connection
	"""
	conn.send(fileName)
	fileSize = str(os.path.getsize(fileName))
	conn.send(fileSize)
	with open(fileName, 'rb') as f:
		byteToSend = f.read(1024)
		conn.send(byteToSend)
		while byteToSend != '':
			byteToSend = f.read(1024)
			conn.send(byteToSend)


def fileReceive(conn):	
	"""Function used for receiving files.
 	   Requires: current dir is correct
 	   			 established socket connection
	"""
	fileName = conn.recv(1024)
	fileSize = conn.recv(1024)
	with open(fileName, 'wb') as f:
		data = conn.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = conn.recv(1024)
			totalRecv += len(data)
			f.write(data)


def fileEncrypt(fileName):
	"""Encrypt sending files."""
	pass
	

# considering adding file compress or decompress
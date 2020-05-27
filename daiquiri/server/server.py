import socket

def fileRecv(sock):
	filename = sock.recv(1024)
	filesize = sock.recv(1024)
	filesize = filesize[4:]
	with open(filename, wb) as f:
		data = s.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < filesize:
			data = s.recv(1024)
			totalRecv += len(data)
			f.write(data)


def Main():
	host = '127.0.0.1'
	port = 5000
	s = socket.socket()
	s.bind((host,port))
	s.listen(5)

	while True:
		c, addr = s.accept
		print('connected to ip {}'.format(addr))
		fileRecv(s)
		
if __name__ == '__main':
	Main()
		
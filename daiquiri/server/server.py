"""Daiquiri server functions."""
import os
import json
import click 
import socket
import threading
from Daiquiri import helper
from Daiquiri.jobs import job

class Server:
	"""Define class Server."""
	
	def __init__(self, port):
		"""Init."""

		"""	
			# donor example
			registeredDonor[0] = {
					 			  donorID: 1,
					 			  host: 'x.x.x.x',
					 			  port: xxxxx,
					 			  local_process_ID: xxxx,
					 			  status: alive/busy/dead,
					 			  device:          ,
					 			  donate_time:        ,
					 			  task: self.tasks[0],
					 			  current_job_ID: xxxxx00001,
					 			  loss: 	
								 }
		"""
		self.registered_donors = []
		self.submitters = []
		self.tasks = []
		self.jobs = []


		# create a TCP socket send and receive message from donor
		self.socket_donors = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_donors.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_donors.bind(('', port)) # current EC2 SG open port: 12345
		self.socket_donors.listen(5)
		
		# create a socket for heartbeat message from donors, UDP
		self.socket_heartbeats = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket_heartbeats.bind(('', port-1))

		# create a TCP socket for submitters' request
		self.socket_submitters = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_submitters.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket_submitters.bind(('', port-2))
		self.socket_submitters.listen(5)		



	def start(self):
		"""Daiquiri server starts."""
		# start a new thread to listen donors' heartbeats
		_thread = threading.Thread(target=self.listenDonorHeartbeats)
		_thread.start()

		# start a new thread to listen submitters' request
		# TODO
		_thread = threading.Thread(target=self.listenSubmitterRequests)
		_thread.start()

		# start a new thread to listen message from donor
		_thread = threading.Thread(target=self.listenDonorMessage)
		_thread.start()

		while True:
			self.donorAllocation()


	def listenDonorMessage(self):
		"""Listen message from donor."""

		# executing all the life time
		while True:
			conn, _ = self.socket_donors.accept()
			message = ''
			while True:
				data = conn.recv(1024)
				message += data.decode('utf-8')
				if len(data) < 1024:
					break
			conn.close()
			message = json.loads(message)

			# handle donor message
			if message['type'] == 'registration':
				self.registerDonor(message)
			elif message['type'] == 'shutdown':
				self.handleDonorShutdown(message)


	def registerDonor(self, message):
		"""Register donor on server."""
		"""
			message example:
			message['type'] can be 
					'registration'/'shutdown'/'assign_job'/'registration_received'
			message = {
						"type": '',
						"host": x.x.x.x,
						"port": xxxx,
						"PID": xx,
						"device": ,
						"time": 
					  }
		"""
		donor = {
			'donorID': len(self.registered_donors),
			'host': message['host'],
			'port': message['port'],
			'localProcessID': message['PID'],
			'status': 'alive',
			'device': message['device'],
			'donate_time': message['time'],
			'task': None,
			'current_job_ID': None,
			'loss': 0		
		}
		self.registered_donors.append(donor)

		# send an acknowledge message back to the donor
		response_message = {
			'type': 'registration_received',
			'host': message['host'],
			'port': message['port'],
			'PID': message['PID'],
			'device': message['device'],
			'time': message['time']
		}

		# donors open a TCP socket connection to listen message from the server
		response_message = json.dumps(response_message)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((message['host'], message['port']))
		s.sendall(response_message.encode('utf-8'))
		s.close()

		# distribute jobs to this new donor machine
		# TODO:
		#distributeJobs()


	def listenSubmitterRequests(self):
		"""Receive requests from submitter."""
		# listen
		c, addr = self.socket_submitters.accept()
		#print('connected to ip {}'.format(addr))

		# 1.create new task
		# 2.check current job status
		# 3.download finished job
		while True:
			message = c.recv(1024)
			if message == 'new':
				if not os.path.exist('~/submiiters/'+str(addr)):
					os.mkdir('~/submiiters/'+str(addr))
				os.chdir('~/submiiters/'+str(addr))
				helper.fileReceive()

				#TODO: somehow create a task message here, no idea
				_task = {}
				self.tasks.append(_task)
				
			
			if message == 'check':
				response_message = checkTaskStatus()
				c.sendall(response_message)

			if message == 'download':
				for f in os.listdir('~/submitter/'+ str(addr) + 'result'):
					helper.fileSend(f)


	def listenDonorHeartbeats(self):
		"""Listen heartbeats message from donor."""

		# listen
		while True:

			# recv msg
			data, _ = self.socket_heartbeats.recvfrom(1024)
			# decode msg
			message = json.loads(data.decode('utf-8'))

			# check the status of this donor
			# if dead -> ignore it
			for donor in self.registered_donors:
				if donor['host'] == message['host']:
					if donor['status'] != 'alive':
						return 

			# reset loss if alive
			for donor in self.registered_donors:
				if donor['host'] == message['host']:
					donor['loss'] = 0


	def donorAllocation(self):
		"""Check donors status and distribute any jobs among alive 
		donors when necessary. This function works whenever a new
		donor registered or a working donor shutdown (connection timeout
		or donor sent a shutdown command).
		"""
		while True:
			
			jobs_not_assigned = []
			avaliable_donors = []
			
			for don in self.registered_donors:
				if don['status'] == 'dead':
					continue
				
				don['loss'] += 1
				if don['loss'] <= 5: 
					avaliable_donors.append(don)
					continue

				# consider the rest donors as 'dead'
				don['status'] = 'dead'

				# TODO: set the 'dead' donors' jobs to be not assigned
				#       and trigger redistribution

				don['task'] = None
				don['current_job_ID'] = None 

			time.sleep(5) # how long should it sleep?

	def handleDonorShutdown(self, message):
		"""Handle the 'shutdown' message sent from donor."""


	def createNewTask(self):
		"""Create new task from submitter."""

		# TODO:
		pass


	def checkTaskStatus(self):
		"""Check current task status from donors' report."""
		# TODO:
		pass


	def sendResult(self):
		"""Send finished task result files back to submitter."""
		pass


	def distributeJobs(self):
		"""Distribute jobs among donors."""
		pass


	def receiveCheckPoint(self):
		"""Receive and store intermediate files from donor."""
		pass


	def estimateJobTime(self):
		"""Estimate time needed for a donor to finish a job."""
		pass


@click.command()
@click.argument("port_num", nargs=1, type=int)
def main(port_num):
    """Starting Daiquiri master server"""
    server = Server(port_num)
    server.start()		


if __name__ == '__main__':
	main()

"""Daiquiri server functions."""
import os
import json 
import socket
import threading
from Daiquiri import helper
from Daiquiri.jobs import job

class Server:
	"""Define class Server."""
	
	def __init__(port):
		"""Init."""

		"""	
			# donor example
			registeredDonor[0] = {
					 			  donorID: 0001,
					 			  host: 'x.x.x.x',
					 			  port: xxxxx,
					 			  #localProcessID: xxxx,
					 			  status: alive/busy/dead,
					 			  Task: [],
					 			  currentJobID: xxxxx00001 	
								 }
		"""
		self.registeredDonor = []
		self.registeredSubmitter = []

		# create a TCP socket
		self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socketTCP.bind(('',port)) # current EC2 SG open port: 12345
		
		# create a new thread for heartbeat message from donors
		self.socketHeartbeat = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP?

		



	def start(self):
		"""Daiquiri server starts."""
		thread = threading.Thread(target=self.listenDonorHeartbeat)
		thread.start()

		while True:
			request = self.listenSubmitterRequest()


	def listenSubmitterRequest(self):
		"""Receive requests from submitter."""
		# listen

		# 1.create new task
		# 2.enquiring current job status
		# 3.download finished job
		pass


	def listenDonorHeartbeat(self):
		"""Listen heartbeat message from donor."""

		# listen
		while True:
			# recv msg
			data, _ = self.socketHeartbeat.recvfrom(1024)
			# decode msg
			  ???
			# update
			handleDonorHeartbeat(data)


	def handleDonorHeartbeat(self):
		"""Handle heartbeat message from donor."""
		pass


	def createNewTask(self):
		"""Create new task from submitter."""
		pass


	def checkTaskStatus(self):
		"""Check current task status from donors' report."""
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

		




import json
import socket
from Socket import Socket
import threading
import os
import sys


class Server(Socket):
	def __init__(self):
		super(Server, self).__init__()
		self.bind(('', 53210))
		self.listen(2)
		print("Server is listening")
		self.f = 0
		self.count = 0
		self.users = []

	def set_up(self):
		
		self.accept_sockets()

	def send_data(self, data, currentuser):
		while len(self.users) < 2:
			print("waiting")
		self.f = 1
		for user in self.users:
			if user != currentuser:
				user.send(data)

	def listen_socket(self, listened_socket = None):
		print("listening user")


		while True:
			data = listened_socket.recv(8192)
			print(threading.active_count(), ", ", len(self.users))
			self.count = threading.active_count()
			#print(f"User {listened_socket} sent {data}")
			#if not (data) and self.f == 1:
			#	print("broken")
				#self.close(listened_socket)
			#	break
			self.send_data(data, listened_socket)


	def accept_sockets(self):
		while True:
			user_socket, address = self.accept()
			print(f"User <{address[0]}> is connected")

			self.users.append(user_socket)
			listen_accepted_user = threading.Thread(
				target = self.listen_socket,
				args = (user_socket,)
				)
			listen_accepted_user.start()

if __name__ == '__main__':
	server = Server()
	server.set_up()


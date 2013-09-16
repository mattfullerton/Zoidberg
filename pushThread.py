import threading
import Queue


class pushThread(threading.Thread):
	def __init__(self, workerQueue, server):
		threading.Thread.__init__(self)
		self.prevStation = ""
		self.workerQueue = workerQueue
		self.server = server
		
		
	def run(self):
		while 1:
			station = self.workerQueue.get()
			
			for clientNumber in self.server.server.clients:
				client = self.server.server.connections[clientNumber]		
				if client.handshaked == True:
					if self.prevStation != station.out():
						client.sendMessage(str(station.out()))
						self.prevStation = station.out()
import signal, sys, ssl
import threading
import pipes
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from optparse import OptionParser

class socketServer(WebSocket):

	def handleMessage(self):
		print "recieved Message"

		if self.data is None:
			self.data = ''
		
		try:
			station = open('pipefile').read()
			self.sendMessage(str(station))
		except Exception as n:
			print n
			
	def handleConnected(self):
		print self.address, 'connected'
		while True:
			station = open('pipefile').read()
			sendMessage(self, station)

	def handleClose(self):
		print self.address, 'closed'



class socketServerThread(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.cls = socketServer
		self.server = SimpleWebSocketServer(host, port, self.cls)
	
	def run(self):
		print "starting Server"
		self.server.serveforever()
		
	def exit(self):
		print "stoping Server"
		self.server.close()

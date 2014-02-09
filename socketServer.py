import threading
import sqlite3
from CallABikeStation import *
from time import sleep
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class socketServer(WebSocket):

	def handleMessage(self):
		print "recieved Message"
		if self.data == 'listAllStations':
			print "listAllStations"
			sqliteConn = sqlite3.connect('pythonABike.db')
			sqliteCursor = sqliteConn.cursor()
			sqliteCursor.execute("SELECT * FROM stations")
			result = sqliteCursor.fetchall()
			for station in result:
				cabStation = CallABikeStation(station[2], station[3], station[4])
				self.socketQueue.put(cabStation)
				sleep(0.025)
			sqliteConn.close()
		
			
						
	def handleConnected(self):
		print self.address, 'connected'

	def handleClose(self):
		print self.address, 'closed'



class socketServerThread(threading.Thread):
	def __init__(self, host, port, socketQueue):
		threading.Thread.__init__(self)
		self.cls = socketServer
		self.socketQueue = socketQueue
		self.server = SimpleWebSocketServer(host, port, self.socketQueue, self.cls)
	
	def run(self):
		print "starting Server"
		self.server.serveforever()
		
	def exit(self):
		print "stoping Server"
		self.server.close()

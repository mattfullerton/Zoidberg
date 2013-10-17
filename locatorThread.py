import threading
import Queue
import sqlite3
import datetime
from time import sleep
from CallABikeStation import *


class locatorThread(threading.Thread):
	def __init__(self, workerQueue, callABike, server, socketQueue):
		threading.Thread.__init__(self)
		self.workerQueue = workerQueue
		self.callABike = callABike
		self.server = server
		self.prevStation = ""
		self.socketQueue = socketQueue
		conn = sqlite3.connect('pythonABike.db')
		c = conn.cursor()
		#c.execute('''DROP TABLE IF EXISTS stations''')
		c.execute('''CREATE TABLE IF NOT EXISTS stations
					(id INTEGER PRIMARY KEY, description, longitude, latitude, isOutside, dateTime)''')
		conn.commit()
		conn.close()
		
	def run(self):
		while 1:
			station = self.workerQueue.get()
	
			if station is None:
				print "Nothing to do here!"
				break;
	
			self.socketQueue.put(station)
			try:
				returnLocations = self.callABike.listReturnLocations('4242', 100, 10000, station.longitude, station.latitude)
				
				if len(returnLocations.Locations) < 100:
					print len(returnLocations.Locations)
					
				#print returnLocations
				conn = sqlite3.connect('pythonABike.db')
				c = conn.cursor()
			
				for location in returnLocations.Locations:
					c.execute("SELECT * FROM stations WHERE longitude = :long AND latitude = :lat", {"long":location.Position.Longitude, "lat":location.Position.Latitude})
					result = c.fetchall()
					if len(result) == 0:
						c.execute("INSERT INTO stations (id, description, longitude, latitude, isOutside, dateTime) VALUES (null, :desc, :long, :lat, :out, strftime('%s', 'now'))", {"desc":location.Description, "long":location.Position.Longitude, "lat":location.Position.Latitude, "out":location.isOutside})
						if location.isOutside != False:
							isOutside = 1
						else:
							isOutside = 0
						newStation = CallABikeStation(location.Position.Longitude, location.Position.Latitude, isOutside)
						self.workerQueue.put(newStation)
				conn.commit()
				conn.close()
				self.workerQueue.task_done()
			except Exception as e:
				print e[0]
				self.workerQueue.put(stations)
				sleep(1)
			
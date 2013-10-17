import sys, os
import threading
import Queue
import signal
import ssl, logging
sys.path.insert(0, "PyABike/")
from PyABike import *
from locatorThread import *
from CallABikeStation import *
from socketServer import *
from pushThread import *

THREADS = 8

workerQueue = Queue.Queue(0)
socketQueue = Queue.Queue(0)
callABike = PyABike()
worker = []


startStation = CallABikeStation(8.403638, 49.006883, 0)
workerQueue.put(startStation)
server = socketServerThread("localhost", 31337, socketQueue)
push = pushThread(socketQueue, server)


# thread for sending data!

# starting threads
for i in range(THREADS):
	thread = locatorThread(workerQueue, callABike, server, socketQueue)
	worker.append(thread)

worker.append(push)
worker.append(server)


for i in worker:
	i.start();


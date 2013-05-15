#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 
import signal,os

signal.signal(signal.SIGPIPE,signal.SIG_IGN)
host = '' 
port1 = 50000 
port2 = 50001
backlog = 5 
size = 1024 

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

print 'Created first TCP socket'

s1.bind((host,port1))

print 'Bound first TCP socket to port ' + str(port1)

s1.listen(backlog) 	

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

print 'Created second TCP socket'

s2.bind((host,port2))

print 'Bound first TCP socket to port ' + str(port2)

s2.listen(backlog) 	

print 'Waiting for 2 incoming connections'

while 1: 
	client1, address1 = s1.accept() 
	print 'Accepted connection from ' + str(address1) 
    
	client2, address2 = s2.accept() 
 	print 'Accepted connection from ' + str(address2) 
	
	try:
		pid = os.fork()
		if (pid>0):
			while 1:
				data = client1.recv(size)
    				if data: 
        				client2.send(data) 
				else:
					print "Peer 1 went away"
					break
		else:
			while 1:
				data = client2.recv(size)
    				if data: 
        				client1.send(data) 
				else:
					print "Peer 2 went away"
					break
	except OSError, e:
        	print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        	sys.exit(1)

	client1.close()
	client2.close()


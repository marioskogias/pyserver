#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 
import signal,os

signal.signal(signal.SIGPIPE,signal.SIG_IGN)
host = '' 
port = 50000 
backlog = 5 
size = 1024 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

print 'Created TCP socket'

s.bind((host,port))

print 'Bound TCP socket to port ' + str(port)

s.listen(backlog) 	

print 'Waiting for an incoming connection'

while 1: 
    client, address = s.accept() 
    print 'Accepted connection from ' + str(address) 
    while 1:
	data = client.recv(size)
    	data = data.upper()
    	if data: 
        	client.send(data) 
	else:
		print "Peer went away"
		break
    client.close()

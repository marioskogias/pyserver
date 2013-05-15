#!/usr/bin/env python

import socket
import sys
import os 

	
if (len(sys.argv) != 3):
	print "Usage: "+ sys.argv[0] + " hostname post"
	sys.exit(1)
	
host = sys.argv[1]
port = int(sys.argv[2])

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Created TCP socket"

try:
	hp = socket.gethostbyname(host)
except:
	print "DNS lookup failed for host" + host
	sys.exit(1)

print "Connecting to remote host ..."
try:
	s.connect((host,port))
except socket.gaierror, e:
	print "Address-related error connecting to server: %s" % e
	sys.exit(1)

print "I say",
print "The remote says".rjust(50)
print "---------------------------------------------------------"
try:
	pid = os.fork()

	if (pid>0):
		while 1:

			text = raw_input()

			text = text+"\0"

			s.sendall(text)
	else:
		while 1:
			data = s.recv(1024)
			data = data	
			print(data.rjust(50))

except OSError, e: 
	print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
	sys.exit(1)

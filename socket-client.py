#!/usr/bin/env python

import socket
import sys
import os 

if (len(sys.argv) != 3):
	print "Usage: "+ sys.argv[0] + " hostname post"
	os._exit(1)
	
host = sys.argv[1]
port = int(sys.argv[2])

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Created TCP socket"

try:
	hp = socket.gethostbyname(host)
except:
	print "DNS lookup failed for host" + host
	os._exit(1)

print "Connecting to remote host ..."
try:
	s.connect((host,port))
except socket.gaierror, e:
	print "Address-related error connecting to server: %s" % e
	os._exit(1)

print "Give me your message..."

text = raw_input()

text = text+"\0"

print "I said " + text

s.sendall(text)

data = s.recv(1024)

print "and the remote said : " + data

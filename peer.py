#!/usr/bin/env python 

import socket 
import sys
import os 
from multiprocessing import Process
import signal

def server():
	port = 50000
	backlog = 5
	size = 1024
	host = ""	
	signal.signal(signal.SIGPIPE,signal.SIG_IGN)	

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	
	sys.stderr.write("Created TCP socket\n")

	try:
		s.bind((host,port)) 
		s.listen(backlog)
	except socket.error:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)	
	
	sys.stderr.write("Bound TCP socket to port " + str(port) + "\n")
	
	client,address=s.accept()
	print "connection from "+str(address)
	return client

def client():
	host = sys.argv[1]
	port = int(sys.argv[2])

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	
	sys.stderr.write("Created TCP socket\n")


	try:
        	hp = socket.gethostbyname(host)
	except socket.error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)

	sys.stderr.write("Connecting to remote host ...\n")
	
	try:
        	s.connect((host,port))
	except socket.gaierror, e:
        	print "Address-related error connecting to server: %s" % e
        	sys.exit(1)

	return s
	

def send(so):	
	while 1:
		text = raw_input()
		text = text+"\0"
		so.sendall(text)

def receive(so):
	while 1:
	
		data = so.recv(1024)
		if data:
			print data.rjust(50)	
                else:
                	print "Peer went away"
                       	os.kill(os.getppid(),signal.SIGKILL)
			os.abort()
	
if ((len(sys.argv) != 3) and  (len(sys.argv) != 2)):
	print "Usage: "+ sys.argv[0] + " <hostname> <port> to join a conversation"
	print "Usage: "+ sys.argv[0] + "server to initianlize a conversation" 
	sys.exit(1)	

if (sys.argv[1]=="server"):
	sock = server()
else:
	sock=client()

print "I say",
print "The remote says".rjust(50)
print "---------------------------------------------------------"

p=Process(target=receive,args=(sock,))
p.start()
send(sock)

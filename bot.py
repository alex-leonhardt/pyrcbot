#! /usr/bin/env python

import sys
import socket
import string
import os
import time

HOST="irc.nap"
PORT=6667
NICK="bot"
IDENT="bot"
REALNAME="Bot"
readbuffer=""
CHANNEL="#chat"

pid = os.fork()

def follow(file):
    file.seek(0,2)      # Go to the end of the file
    while True:
         line = file.readline()
         if not line:
             time.sleep(0.2)    # Sleep briefly
             continue
         yield line

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(2)
s.send("JOIN %s\r\n" % CHANNEL)
s.send("PRIVMSG %s :%s\r\n" % (CHANNEL, "your friendly neighborhood bot is back!"))

ircinput = open("/tmp/irc.input")

if (pid == 0):

  pid2 = os.fork()
  if (pid2 == 0): 
    loglines = follow(ircinput)
    for line in loglines:
	    s.send("PRIVMSG %s :%s\r\n" % (CHANNEL, line))

  pid3 = os.fork()
  if (pid3 == 0):
    while 1:
      readbuffer=readbuffer+s.recv(1024)
      temp=string.split(readbuffer, "\n")
      print temp
      readbuffer=temp.pop( )

      for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
      if (line[0]=="PING"):
        s.send("PONG %s\r\n" % line[1])


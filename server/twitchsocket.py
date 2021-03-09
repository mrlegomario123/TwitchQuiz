import signal, sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import threading

import json
import re

from quizLogic import *

xclient = None
twitchConnector = None

def callback(stri, client_id):
	xclient.callback(stri, client_id)

PORTNUM = 9006

#quiz = QuizLogic()
#quiz.setSocketCallback(callback, "12345")

# Websocket class to echo received data

#==== HANDLING MSGS FROM HTML ====

#echo: class passed when starting ws server, contains methods to call when events occur
#e.g. handleMessage, handleConnected
class Echo(WebSocket):

	#called
	def handleMessage(self):
		#print("Echoing '%s'" % self.data)
		#self.sendMessage("12345")


		mess = json.loads(self.data)
		if twitchConnector != None:
			twitchConnector.receiveMessage(mess)

	'''
		if mess['command'] == 'fromtwitch':
			response = mess['payload']
			CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
			username = re.search(r"\w+", response).group(0)  # return the entire match
			twmessage = CHAT_MSG.sub("", response)
			print(username + ": " + twmessage)
			#quiz.recieveCommand(username, twmessage)
	'''
	#as soon as client connects to this ws server, this method is called
	#when client connects, sets instance of self to xclient to access later
	def handleConnected(self):
		global xclient
		xclient = self
		print("Connected")

	def handleClose(self):
		print("Disconnected")

	def callback(self, stri, client_id):
		self.sendMessage(stri)

#==== STARTING WEBSOCKET SERVER ====

class twitchSocket:

	def __init__(self, tc):
		print("Websocket server on port %s" % PORTNUM)
		global twitchConnector
		twitchConnector = tc
		#starts websocket server listening on port 9006 (websocket allocated port)
		#means when data is sent to the ip adress of this device on port 9006, does something with the message
		#server just listens, up to client to create connection i.e. enter ip adress of server to send data
		self.server = SimpleWebSocketServer('', PORTNUM, Echo)

		# This looks for CTRL-C
		signal.signal(signal.SIGINT, self.close_server)

	#creates new thread with start server method to run on the new thread
	#allows to run this blocking task in the background
	def startAll(self):
		t = threading.Thread(target=self.serve)
		t.start()

	def serve(self):
		self.server.serveforever()

	def callback(self, stri, client_id):
		global xclient
		if xclient != None:
			xclient.callback(stri, client_id)

	def close_server(self, signal, frame):
		self.server.close()
		sys.exit()





''' 
# Handle ctrl-C: close server
def close_server(signal, frame):
	server.close()
	sys.exit()

quiz = QuizLogic()
quiz.setSocketCallback(callback, "12345")

if __name__ == "__main__":
	print("Websocket server on port %s" % PORTNUM)
	server = SimpleWebSocketServer('', PORTNUM, Echo)

	signal.signal(signal.SIGINT, close_server)
	server.serveforever()
'''
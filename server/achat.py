import socket
import time
import re
import logging

from quizLogic import *
from twitchsocket import *

#==== CONFIGURING CONNECTION VARS ====

HOST = "irc.chat.twitch.tv"  # the twitch irc server
PORT = 6667  # always use port 6667
NICK = "captainpovey"  # twitch username, lowercase
CHAN = "#" + NICK  # the channel you want to join

# To get the key, I used : https://twitchapps.com/tmi/
PASS = "oauth:gklkezewnbvu7hi92uqijbgqgvu5vf"  # your twitch OAuth token

# Message Rate
RATE = (20 / 30)  # messages per second

# bot.py portion
# Network functions go here

#==== ESTABLISH CONNECTION ====

s = socket.socket() #uses library to create socket
s.connect((HOST, PORT)) #connect to host (irc.chat.twitch.tv) on port (6667)
#send oauth + username + channel name -> twitch to authenicate
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

def chat(sock, msg):
    '''
    Send a chat message to the server.
    sock -- the socket over which to send the message
    msg -- the message to be sent
    '''
    sock.send("PRIVMSG #{} :{}".format(CHAN, msg))

# regular expressions to reformat string sent in from twitch into usable format
# Make sure you prefix the quotes with an 'r'
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

class TwitchConnector:

    def receiveMessage(self, data):
        datas = quiz.recieveWebSocketCommand(data)
        if datas != None:
            ts.callback(datas, None)

twitchConnector = TwitchConnector()
quiz = QuizLogic()

#==== MAIN LISTENING LOOP ====

ts = twitchSocket(twitchConnector)
ts.startAll()

try:
    while True:
        #listens for message
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
           s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
           print("Pong")
        else:
            #otherwise, twitch message, decodes
            username = re.search(r"\w+", response).group(0)  # gets username
            message = CHAT_MSG.sub("", response).rstrip()
            print(username + ": " + message)
            #quizlogic processes chat msg, and returns json string about new game state
            #e.g. when new player joins, {"command":"join", "payload" : {"username" : username})
            #can then process this to e.g. pass to html
            datas = quiz.recieveCommand(username, message)
            #callback to pass back to html via websocket
            #only sends data back to html if return data to be sent from quizlogic
            if datas != None:
                ts.callback(datas, None)

    '''
        if 'hello fuzzy' in message:
            omess = "PRIVMSG #" + NICK + " : Hello to you too\r\n"
            s.send(omess.encode("utf-8"))
    '''
except:
    logging.exception('error during handling user data')
    self.close(status=1011, reason='Internal server error')

time.sleep(1 / RATE)

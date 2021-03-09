import socket
import time
import re

HOST = "irc.chat.twitch.tv"  # the twitch irc server
PORT = 6667  # always use port 6667
NICK = "captainpovey"  # twitch username, lowercase
CHAN = "#" + NICK  # the channel you want to join

# To get the key, I used : https://twitchapps.com/tmi/
PASS = "oauth:vin2a9d44m18tavjyojemj3k1e1ta7"  # your twitch OAuth token

# Message Rate
RATE = (20 / 30)  # messages per second

# bot.py portion
# Network functions go here

s = socket.socket()
s.connect((HOST, PORT))
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


def ban(sock, user):
    '''
    Ban a user from the current channel.
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    '''
    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=10):
    '''
    Time out a user for a set period of time
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    '''
    chat(sock, ".timeout {}".format(user, secs))

# Make sure you prefix the quotes with an 'r'
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


while True:
    response = s.recv(1024).decode("utf-8")
    #print(response)
    if response == "PING :tmi.twitch.tv\r\n":
       s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
       print("Pong")
    else:
        username = re.search(r"\w+", response).group(0)  # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)

    if 'hello fuzzy' in message:
        omess = "PRIVMSG #" + NICK + " : Hello to you too\r\n"
        s.send(omess.encode("utf-8"))

    time.sleep(1 / RATE)

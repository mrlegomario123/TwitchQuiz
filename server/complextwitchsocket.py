# pip3 install asyncio
# pip3 install websockets

import asyncio
import websockets
import json
import re

from quizLogic import *

async def callback(stri, client_id):
	print("Hello from callback")
	print(stri)
	await tell(client_id, stri)

# Get a port that a connection connected with
# We use the port as a simple connection ID
def get_port(websocket):
    return websocket.remote_address[1]

# Send a message to a client
async def tell(client_id, message):

    # Make sure the client id is a string
    client_id = str(client_id)
    print("Telling " + client_id)

    # Go through the connections
    for user in connections:
        # If the connection id is this id
        # This relies on the id being an int
        if get_port(user) == int( client_id ):
            print("Sending messge " + message)
            await user.send(message)

connections = []

async def register(websocket):
	connections.append(websocket)

async def unregister(websocket):
	pass

async def logic(websocket, path):
	print("Starting")

	await register(websocket)

	# Gets an unique ID of the connected client
	# Using the incoming port
	client_id = get_port(websocket)

	try:
		async for message in websocket:
			mess = json.loads(message)

			if mess['command'] == 'fromtwitch':
				response = mess['payload']
				CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
				username = re.search(r"\w+", response).group(0)  # return the entire match
				twmessage = CHAT_MSG.sub("", response)
				print(username + ": " + twmessage)

				quiz.recieveCommand(username, twmessage)

			print("Got message : " + message)
	except websockets.ConnectionClosed as e:
		print("ConnectionClosed");

	finally:
		print("Unregistering")
		await unregister(websocket)

#quiz.startGame()

quiz = QuizLogic(callback, "client_id")
client_id = None
start_server = websockets.serve(logic, "localhost", "9006")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

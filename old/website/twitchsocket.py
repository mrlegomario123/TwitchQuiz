# pip3 install asyncio
# pip3 install websockets

import asyncio
import websockets
import time

connections = []

async def register(websocket):
	connections.append(websocket)

async def unregister(websocket):
	pass

async def logic(websocket, path):
	print("Starting")
	await register(websocket)
	try:
		async for message in websocket:
			print("Got message : " + message)
	except websockets.ConnectionClosed as e:
		print("ConnectionClosed");

	finally:
		print("Unregistering")
		await unregister(websocket)

start_server = websockets.serve(logic, "localhost", "9006")

asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()

def main_loop():
	print("Loo")
	time.sleep(2)

print("1")
async def dof():
	await main_loop()

dof()
print("2")
asyncio.create_task(main_loop())

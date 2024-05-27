import socket
import asyncio

async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        response = str(eval(request)) + '\n'
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15555)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())

class GameBroadcaster:
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # aktiviere broadcast funktion

        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(("0.0.0.0", 5000))
        asyncio.run(self.receive())

    async def handle_client(client):
        loop = asyncio.get_event_loop()
        request = None
        while request != 'quit':
            request = (await loop.sock_recv(client, 255)).decode('utf8')
            response = str(eval(request)) + '\n'
            await loop.sock_sendall(client, response.encode('utf8'))
        client.close()

    async def receive(self):
        while True:
            data, addr = self.receiver.recvfrom(100)
            print(f"empfange Daten: {data.decode()}")




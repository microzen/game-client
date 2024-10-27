import asyncio
import ctypes
import socket


class GameClient:

    def __init__(self, address, port):
        self.client = None
        self.data = None
        self.address = address
        self.server_port = port
        self.is_ready = ctypes.c_bool(False)

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setblocking(False)
        self.client.connect((self.address, self.server_port))
        # await asyncio.get_running_loop().sock_connect(self.client, (self.address, self.server_port))
        print("Connected to server.")

    def send(self, data):
        data += "\n"
        self.client.sendall(data.encode('utf-8'))

    def receive(self):
        if self.is_ready.value:
            self.is_ready.value = False
            return self.data
        else:
            return None

    def receive_task(self):
        # loop = asyncio.get_running_loop()
        try:
            while True:
                # self.data = await loop.sock_recv(self.client, 1024)
                self.data = self.client.recv(1024)
                if not self.data:
                    print("Server closed the connection.")
                    break
                print("Received:", self.data.decode())
                self.is_ready.value = True
        except Exception as e:
            print("Error receiving data:", e)
        finally:
            self.is_ready.value = False


import asyncio

from socket import *
from _thread import *

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


class SocClient:
    __slots__ = ['cliSocket']

    def __init__(self):
        self.cliSocket = socket(AF_INET, SOCK_STREAM)

    def exec_client(self, addr='localhost', port=8080):
        try:
            self.cliSocket.connect((addr, port))

            nickname = input("Type your nickname>> ")
            self.cliSocket.send(nickname.encode())

            start_new_thread(self.threaded_recv, ())

            asyncio.run(self.send_message(nickname))

            self.cliSocket.close()
            print("Closed chatroom successfully.")

        finally:
            self.cliSocket.close()

    def threaded_recv(self):
        try:
            while True:
                data = self.cliSocket.recv(1024)
                dec = data.decode()

                if dec == "quit":
                    break
                print(dec)

            self.cliSocket.close()

        except Exception as e:
            pass

    async def send_message(self, nickname):
        session = PromptSession(message=nickname + ": ")
        with patch_stdout():
            while True:
                message = await session.prompt_async()
                if message == "quit":
                    break

                self.cliSocket.send(message.encode())

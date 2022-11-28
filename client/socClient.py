import asyncio

from socket import *
from _thread import *

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


class SocClient:
    __slots__ = ['cliSocket']

    def __init__(self):
        # instance variables
        # cliSocket: a client-side socket
        self.cliSocket = socket(AF_INET, SOCK_STREAM)

    def exec_client(self, addr='localhost', port=8080):
        try:
            # establish a connection
            self.cliSocket.connect((addr, port))

            # As the connection is established,
            # get a nickname for the chatroom and send it to the server.
            nickname = input("Type your nickname>> ")
            self.cliSocket.send(nickname.encode())

            # open a new thread to get asynchronous messages
            # from the client-side socket
            start_new_thread(self.threaded_recv, ())

            # to avoid being interrupted by coroutine in the thread,
            # when input string is formatted, I used asyncio and prompt_toolkit
            asyncio.run(self.send_message(nickname))

            self.cliSocket.close()
            print("Closed chatroom successfully.")

        finally:
            self.cliSocket.close()

    def threaded_recv(self):
        # a method called when the thread starts.
        # receive chat data and print it to client console.
        try:
            while True:
                # receive the data and decode it to normal string
                data = self.cliSocket.recv(1024)
                if not data:
                    print("Server disconnected!")
                    break
                dec = data.decode()

                print(dec)

            self.cliSocket.close()

        except Exception as e:
            pass

    async def send_message(self, nickname):
        # the function for input interface
        # that keeps the input message from being broken
        # by newly arrived chat data.

        # create PromptSession
        session = PromptSession(message=nickname + ": ")
        with patch_stdout():
            while True:
                # get async data from the prompt
                message = await session.prompt_async()

                # when the message is "quit",
                # the user quit from the chatroom
                if message == "quit":
                    break

                self.cliSocket.send(message.encode())

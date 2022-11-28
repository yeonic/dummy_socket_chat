from socket import *
from _thread import *


class SocClient:
    __slots__ = ['cliSocket']

    def __init__(self):
        self.cliSocket = socket(AF_INET, SOCK_STREAM)

    def exec_client(self, addr='localhost', port=8080):
        self.cliSocket.connect((addr, port))

        nickname = input("Type your nickname>>")
        self.cliSocket.send(nickname.encode())

        start_new_thread(self.threaded_recv, ())

        while True:
            message = input(">>>")
            if message == "quit":
                break

            self.cliSocket.send(message.encode())

        self.cliSocket.close()
        print("Closed chatroom successfully.")

    def threaded_recv(self):
        while True:
            data = self.cliSocket.recv(1024)
            print(data.decode(), end='')

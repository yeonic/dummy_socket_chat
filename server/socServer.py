from socket import *
from user import *
from _thread import *


class SocServer:
    __slots__ = ["sevSocket", "connected_users"]

    def __init__(self):
        self.sevSocket = socket(AF_INET, SOCK_STREAM)
        self.connected_users = []

    def up_server(self, port=8080, n_of_client=3):
        # this dummy server will only be used in localhost
        print(">>> Server is up on PORT:" + str(port))
        self.sevSocket.bind(('localhost', port))
        self.sevSocket.listen(n_of_client)

        try:
            while True:
                print(">>> Waiting for clients...\n# of activated users: " + str(len(self.connected_users)))
                (client, addr) = self.sevSocket.accept()
                start_new_thread(self.accept_client_threaded, (client, addr))

        finally:
            self.sevSocket.close()
            print("Socket closed in unexpected way.")

    def propagate(self, now_user, message):
        for other in self.connected_users:
            if other is not now_user:
                other.client.send(message)
        print(">>> Message successfully propagated.")

    def accept_client_threaded(self, client: socket, addr):
        # get nickname and append to connected list
        nick = client.recv(1024)
        now_user = User(nick.decode(), client, addr)
        self.connected_users.append(now_user)

        # print message to the server console
        message = now_user.nickname + "(" + str(addr[0]) + ":" + str(addr[1]) + ") has joined the chatroom!!\n"
        print(message, end='')

        # send the welcome message to the client
        client.send(">>> You have joined the chatroom now.\n".encode())

        # and send the message to the other clients
        self.propagate(now_user, message.encode())

        while True:
            try:
                chat = client.recv(1024)
                temp_chat = (now_user.nickname + ": " + chat.decode() + '\n')

                if not chat:
                    message = "User \"" + now_user.nickname + "\" left chatroom.\n"
                    print(message, end='')
                    self.propagate(now_user, message.encode())
                    break

                print("chat received from " + now_user.nickname + "(" + str(addr[0]) + ":" + str(addr[1]) + ")")
                self.propagate(now_user, temp_chat.encode())

            except ConnectionResetError as e:
                print("Error occurred: " + e)
                print("Close connection.")
                break

        if now_user in self.connected_users:
            self.connected_users.remove(now_user)

        client.close()




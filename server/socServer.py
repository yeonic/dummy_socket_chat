from socket import *
from user import *
from _thread import *


class SocServer:
    __slots__ = ["sevSocket", "connected_users"]

    def __init__(self):
        # instance variables
        # sevSocket: server-side socket
        # connected_users: array of instance of class User
        # -> for propagation of messages, formatting messages, and counting participants
        self.sevSocket = socket(AF_INET, SOCK_STREAM)
        self.connected_users = []

    def up_server(self, port=8080, n_of_client=3):
        # this dummy server will only be used in localhost
        # default number of clients to listen is 3
        print(">>> Server is up on PORT:" + str(port))
        self.sevSocket.bind(('localhost', port))
        self.sevSocket.listen(n_of_client)

        try:
            while True:
                # accept client and open new thread
                # calling accept_client_threaded method
                print(">>> Waiting for clients...")
                (client, addr) = self.sevSocket.accept()
                start_new_thread(self.accept_client_threaded, (client, addr))

        finally:
            self.sevSocket.close()
            print("Socket closed in unexpected way.")

    def propagate(self, now_user, message):
        for other in self.connected_users:
            if other is not now_user:
                other.client.send(message)
        print(">>> Message successfully propagated.\n")

    def accept_client_threaded(self, client: socket, addr):
        # get nickname and append to connected list
        nick = client.recv(1024)
        now_user = User(nick.decode(), client, addr)
        self.connected_users.append(now_user)

        # print join message to the server console
        message = now_user.nickname + "(" + str(addr[1]) + ") has joined the chatroom!!"
        message += "\nNow participants: " + str(len(self.connected_users))
        print(message)

        # send the welcome message to the current client
        client.send(">>> You have joined the chatroom now.\n".encode())

        # and send the join message to the other clients
        self.propagate(now_user, ("\n"+message+"\n").encode())

        while True:
            try:
                # receive the chat data from the client
                # and format the chat data to "nickname(port): message"
                chat = client.recv(1024)
                temp_chat = now_user.nickname + "(" + str(now_user.addr[1]) + "): " + chat.decode()

                if not chat:
                    # if the connection is not alive anymore
                    # propagate the message to the other participants
                    message = "User \"" + now_user.nickname + "\" left chatroom."
                    print(message)
                    self.propagate(now_user, message.encode())
                    break

                # if the data received correctly
                # print related message to the server console, and propagate the formatted chat data.
                print("chat received from " + now_user.nickname + "(" + str(addr[0]) + ":" + str(addr[1]) + ")")
                self.propagate(now_user, temp_chat.encode())

            except ConnectionResetError as e:
                print("Error occurred: " + e)
                print("Close connection.")
                break

        if now_user in self.connected_users:
            # when the socket finished the connection,
            # remove the corresponding User from the self.connected_users
            self.connected_users.remove(now_user)
            print("Now participants: " + str(len(self.connected_users)))

        client.close()




from socket import *
from _thread import *


class SocServer:
    __slots__ = ["sevSocket", "connected_clients"]

    def __init__(self):
        self.sevSocket = socket(AF_INET, SOCK_STREAM)
        self.connected_clients = []

    def up_server(self, port=8080, n_of_client=3):
        # this dummy server will only be used in localhost
        print(">>> Server is up on PORT:" + str(port))
        self.sevSocket.bind(('localhost', port))
        self.sevSocket.listen(n_of_client)

        try:
            while True:
                print(">>> Waiting for clients")
                (client, addr) = self.sevSocket.accept()
                self.connected_clients.append(client)
                start_new_thread(self.client_accept_threaded, (client, addr))

        except Exception as e:
            pass

        finally:
            self.sevSocket.close()

    def client_accept_threaded(self):
        pass



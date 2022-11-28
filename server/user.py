class User:
    __slots__ = ["client", "nickname", "addr"]

    def __init__(self, nickname, client, addr):
        # instance variables
        # client: client-side socket
        # nickname: nickname received from client
        # addr: addr[0] is IP address && addr[1] is port address

        self.client = client
        self.nickname = nickname
        self.addr = addr

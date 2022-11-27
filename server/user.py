class User:
    __slots__ = ["client", "nickname", "addr"]

    def __init__(self, nickname, client, addr):
        self.client = client
        self.nickname = nickname
        self.addr = addr

import socket

class GameBroadcaster:
    def __init__(self, port=5000):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # aktiviere broadcast funktion
        self.lokal_ip = socket.gethostbyname(socket.gethostname())

        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(("0.0.0.0", port))
        self.receiver.setblocking(False)
        self.broadcast_address = ("255.255.255.255", port)

    def broadcast_game(self, serialized_game: str):
        self.sender.sendto(serialized_game.encode(), self.broadcast_address)

    def receive_game_broadcasts(self) -> (str, str):
        try:
            data, addr = self.receiver.recvfrom(1500000)
            if addr[0] == self.lokal_ip:
                # this is our own broadcast - irgnore
                data, addr = self.receiver.recvfrom(1500000)
            return data.decode(), str(addr)
        except BlockingIOError:
            return None, None

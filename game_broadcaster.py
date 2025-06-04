import socket


class GameBroadcaster:
    def __init__(self, port=5000):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # aktiviere broadcast funktion
        self.lokal_ip = get_ip()

        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(("0.0.0.0", port))
        self.receiver.setblocking(False)
        self.broadcast_address = ("255.255.255.255", port)

    def broadcast_game(self, serialized_game: str):
        # self.sender.sendto(serialized_game.encode(), self.broadcast_address)
        # Aufgabe
        pass

    def receive_game_broadcasts(self) -> (str, str):
        try:
            data, addr = self.receiver.recvfrom(1500000)
            if addr[0] == self.lokal_ip:
                # this is our own broadcast - irgnore
                data, addr = self.receiver.recvfrom(1500000)
            return data.decode(), str(addr)
        except BlockingIOError:
            return None, None


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


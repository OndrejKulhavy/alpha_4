import socket
import threading

from src.configuration.config import Config
from src.data_classes.peer import Peer


class TCP:
    def __init__(self, config: Config):
        self.connections = {}
        self.config = config

    def establish_connection(self, peer: Peer):
        if peer in self.connections:
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer.ip_address, self.config.tcp_settings.port))
            self.connections[peer] = s
        except Exception as e:
            print(e)

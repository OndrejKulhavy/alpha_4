from src.configuration.config import Config
from src.configuration.shared_collection import SharedPeerCollection
from src.udp.udp import UDP


def main():
    peer_connections = SharedPeerCollection()
    config = Config("config.ini")
    UDP(config, peer_connections)

if __name__ == "__main__":
    main()

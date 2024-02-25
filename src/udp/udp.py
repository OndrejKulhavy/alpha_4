import json
import socket
import threading
import time

from src.configuration.config import Config
from src.configuration.shared_collection import SharedPeerCollection
from src.data_classes.peer import Peer


class UDP:
    def __init__(self, config: Config, peers: SharedPeerCollection):
        """
        Initializes the UDP class.

        Parameters:
        - config (Config): Configuration settings for the UDP communication.
        - peers (SharedPeerCollection): Shared collection to store information about discovered peers.

        Initializes a thread to run the UDP communication in the background.
        """
        self.peers = peers
        self.config = config
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def send_discovery_message(self, sock):
        """
        Sends a discovery message to discover peers on the network.

        Parameters:
        - sock (socket): The UDP socket for communication.

        Sends a "hello" command with the peer ID to the specified address and port.
        """
        init_message = json.dumps({"command": "hello", "peer_id": self.config.other_settings.peer_id}).encode("utf-8")
        sock.sendto(init_message, (self.config.udp_settings.address, self.config.udp_settings.port))
        print("Sending discovery message...")
        print("To address: ", self.config.udp_settings.address + ":" + str(self.config.udp_settings.port))

    def handle_response(self, sock, data, addr):
        """
        Handles the response received from a peer after sending a discovery message.

        Parameters:
        - sock (socket): The UDP socket for communication.
        - data (bytes): Received data from the peer.
        - addr (tuple): Address of the peer.

        Processes the response data and adds the peer to the shared collection if the response is valid.
        """
        response = json.loads(data.decode("utf-8"))
        if response.get("command") == "hello":
            self.send_reply(sock)

        if response.get("status") == "ok":
            print(response)
            peer = Peer(id=response.get("peer_id"), ip_address=addr[0])
            self.peers.add(peer)
            print(peer)
            print(self.peers.get_all())

    def send_reply(self, sock):
        """
        Sends a reply to acknowledge a valid discovery message.

        Parameters:
        - sock (socket): The UDP socket for communication.

        Sends a "status: ok" reply with the peer ID to the specified address and port.
        """
        reply_message = json.dumps({"status": "ok", "peer_id": self.config.other_settings.peer_id}).encode("utf-8")
        sock.sendto(reply_message, (self.config.udp_settings.address, self.config.udp_settings.port))
        print("Sending reply...")

    def run(self):
        """
        Runs the UDP communication in a background thread.

        Creates and configures the UDP socket, sends discovery messages, and handles responses.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1.0)  # Set a timeout for receiving messages

        print("UDP thread started")

        while True:
            self.send_discovery_message(sock)

            start_time = time.time()
            while time.time() - start_time < 5:
                try:
                    data, addr = sock.recvfrom(1024)
                    self.handle_response(sock, data, addr)
                except socket.timeout:
                    pass

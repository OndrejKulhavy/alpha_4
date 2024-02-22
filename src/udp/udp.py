import socket
import json
import time

from src.configuration import config
from src.configuration.config import read_config


class UDP:
    def __init__(self):
        self.config = read_config().udp

    def send_udp_query(self):
        query = {"command": "hello", "peer_id": self.config.peer_id}
        query_json = json.dumps(query)
        encoded_query_json = query_json.encode('utf-8')
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(encoded_query_json, (self.config.udp.broadcast_address, self.config.udp.port))

    def handle_udp_response(self, response_json):
        try:
            response = json.loads(response_json)
            if response.get("status") == "ok" and response.get("peer_id") != self.peer_id:
                print(f"Received response from peer: {response['peer_id']}")
                # Extract IP address from the response and establish TCP connection if needed
                # Implement your TCP connection logic here
        except json.JSONDecodeError:
            print("Error decoding UDP response JSON.")

    def run_discovery(self):
        while True:
            self.send_udp_query()

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('', self.udp_port))
                s.settimeout(self.discovery_interval)

                try:
                    while True:
                        data, addr = s.recvfrom(1024)
                        response_json = data.decode('utf-8')
                        self.handle_udp_response(response_json)
                except socket.timeout:
                    pass

            time.sleep(self.discovery_interval)

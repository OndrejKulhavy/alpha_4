import socket
import json
import time
from src.configuration.config import read_config


class UDP:
    def __init__(self, peer_id):
        config = read_config()
        self.peer_id = config
        self.peer_id = peer_id
        self.udp_port = 9876
        self.udp_broadcast_address = '<broadcast>'
        self.discovery_interval = 5

    def send_udp_query(self):
        query = {"command": "hello", "peer_id": self.peer_id}
        query_json = json.dumps(query)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(query_json.encode('utf-8'), (self.udp_broadcast_address, self.udp_port))

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

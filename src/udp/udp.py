import json
import socket
import threading
import time

from src.configuration.config import Config


class UDP():
    def __init__(self, config: Config):
        self.config = config
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.thread.join()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        init_message = json.dumps({"command": "hello", "peer_id": self.config.other.peer_id}).encode("utf-8")
        reply_message = json.dumps({"status": "ok", "peer_id": self.config.other.peer_id}).encode("utf-8")

        print("UDP thread started")

        while True:
            print("Sending discovery message...")
            sock.sendto(
                init_message,
                (self.config.udp.address, self.config.udp.port),
            )

            print("Receiving replies for 5 seconds...")
            start_time = time.time()
            while time.time() - start_time < 5:
                try:
                    data, addr = sock.recvfrom(1024)
                    response = json.loads(data.decode("utf-8"))
                    print(f"Received response from {addr}: {response}")
                    if response["command"] == "hello":
                        print("Sending reply...")
                        sock.sendto(
                            reply_message,
                            (self.config.udp.address, self.config.udp.port),
                        )
                except socket.timeout:
                    pass

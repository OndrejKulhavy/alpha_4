import socket
import json
import threading

# Constants
DEFAULT_PORT = 9876
BROADCAST_ADDR = "172.31.255.255"


def udp_discovery():
    """
    Function for UDP discovery.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))

        if message['command'] == 'hello':
            print(f"Objeven peer {message['peer_id']} na {addr[0]}")
            # Implement further actions here, e.g., store discovered peers,
            # connect to them via TCP, etc.


if __name__ == '__main__':
    thread = threading.Thread(target=udp_discovery)
    thread.start()
    thread.join()  # Wait for thread to finish

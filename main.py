import socket
import json
import threading
import time

# Constants
DEFAULT_PORT = 9876
BROADCAST_ADDR = "172.31.255.255"
DISCOVERY_INTERVAL = 5  # Seconds between discovery broadcasts


def udp_discovery():
    """
    Function for UDP discovery.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        # Send discovery message
        message = json.dumps({'command': 'hello', 'peer_id': PEER_ID}).encode('utf-8')
        sock.sendto(message, (BROADCAST_ADDR, DEFAULT_PORT))

        # Receive responses for 1 second
        start_time = time.time()
        while time.time() - start_time < 1:
            try:
                data, addr = sock.recvfrom(1024)
                response = json.loads(data.decode('utf-8'))
                if response['status'] == 'ok':
                    print(f"Objeven peer {response['peer_id']} na {addr[0]}")
                    # Implement further actions here, e.g., store discovered peers,
                    # connect to them via TCP, etc.
            except socket.timeout:
                pass

        # Wait before next broadcast
        time.sleep(DISCOVERY_INTERVAL)


if __name__ == '__main__':
    PEER_ID = input("Zadejte své ID: ")  # Get unique peer ID
    thread = threading.Thread(target=udp_discovery)
    thread.start()
    thread.join()  # Wait for thread to finish

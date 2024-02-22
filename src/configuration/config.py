from collections import namedtuple
import configparser

UDPConfig = namedtuple("UDPConfig", ["broadcast_port", "broadcast_interval", "broadcast_adress"])
TCPConfig = namedtuple("TCPConfig", ["listen_port", "timeout"])
HTTPConfig = namedtuple("HTTPConfig", ["api_port"])
PeerConfig = namedtuple("PeerConfig", ["peer_id", "max_messages"])

ConfigTemplate = namedtuple("Config", ["udp", "tcp", "http", "peer"])


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    udp_broadcast_port = config.getint("UDP", "broadcast_port")
    udp_broadcast_interval = config.getint("UDP", "broadcast_interval")
    udp_broadcast_address = config.get("UDP", "broadcast_address")

    tcp_listen_port = config.getint("TCP", "listen_port")
    tcp_timeout = config.getint("TCP", "timeout")

    http_api_port = config.get("HTTP", "api_port")

    peer_id = config.get("Peer", "peer_id")
    max_messages = config.getint("Peer", "max_messages")

    udp_config = UDPConfig(
        broadcast_port=udp_broadcast_port,
        broadcast_interval=udp_broadcast_interval,
        broadcast_adress=udp_broadcast_address,
    )
    tcp_config = TCPConfig(
        listen_port=tcp_listen_port,
        timeout=tcp_timeout
    )
    http_config = HTTPConfig(
        api_port=http_api_port
    )
    peer_config = PeerConfig(
        peer_id=peer_id,
        max_messages=max_messages
    )

    return ConfigTemplate(
        udp=udp_config,
        tcp=tcp_config,
        http=http_config,
        peer=peer_config
    )

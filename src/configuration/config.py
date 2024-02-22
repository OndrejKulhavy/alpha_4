from collections import namedtuple
import configparser

UDPConfig = namedtuple("UDPConfig", ["broadcast_port", "broadcast_interval"])
TCPConfig = namedtuple("TCPConfig", ["listen_port", "timeout"])
HTTPConfig = namedtuple("HTTPConfig", ["api_port"])
OtherConfig = namedtuple("OtherConfig", ["peer_id", "max_messages"])

ConfigTemplate = namedtuple("Config", ["udp", "tcp", "http", "other"])


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    udp_broadcast_port = config.getint("UDP", "broadcast_port")
    udp_broadcast_interval = config.getint("UDP", "broadcast_interval")

    tcp_listen_port = config.getint("TCP", "listen_port")
    tcp_timeout = config.getint("TCP", "timeout")

    http_api_port = config.getint("HTTP", "api_port")

    peer_id = config.get("Peer", "peer_id")
    max_messages = config.getint("Peer", "max_messages")

    udp_config = UDPConfig(
        broadcast_port=udp_broadcast_port,
        broadcast_interval=udp_broadcast_interval
    )
    tcp_config = TCPConfig(
        listen_port=tcp_listen_port,
        timeout=tcp_timeout
    )
    http_config = HTTPConfig(
        api_port=http_api_port
    )
    other_config = OtherConfig(
        peer_id=peer_id,
        max_messages=max_messages
    )

    return ConfigTemplate(
        udp=udp_config,
        tcp=tcp_config,
        http=http_config,
        other=other_config
    )

import socket
import json
import threading
import time

from src.configuration.config import Config
from src.udp.udp import UDP


def main():
    config = Config("config.ini")
    udp = UDP(config)


if __name__ == '__main__':
    main()

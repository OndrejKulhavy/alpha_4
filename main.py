from flask import Flask

from src.udp.udp import UDP


def main():
    udp = UDP()
    udp.run_discovery()


if __name__ == "__main__":
    main()

import re
from dataclasses import dataclass


@dataclass
class Peer:
    id: str
    ip_address: str

    def __post_init__(self):
        regex = r"(\b24[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
        if re.match(regex, self.ip_address) is None:
            raise ValueError("Invalid IP address")

import re
from dataclasses import dataclass
from re import match


@dataclass(frozen=True)
class HTTPConfig:
    """Configuration for HTTP-related settings."""
    api_port: int


@dataclass(frozen=True)
class OtherConfig:
    """Configuration for other settings."""

    peer_id: str
    max_messages: int


@dataclass(frozen=True)
class TCPConfig:
    """Configuration for TCP-related settings."""

    port: int
    timeout: int


@dataclass(frozen=True)
class UDPConfig:
    """Configuration for UDP-related settings."""

    port: int
    interval: int
    address: str

    def __post_init__(self):
        if self.interval < 1:
            raise ValueError("Interval must be greater than 0")

        if self.port < 1 or self.port > 65535:
            raise ValueError("Port must be between 1 and 65535")

        regex = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
        if re.match(regex, self.address) is None:
            raise ValueError("Invalid IP address")

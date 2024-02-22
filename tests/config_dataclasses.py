import pytest
from dataclasses import dataclass
import re
from src.configuration.sections import UDPConfig


def test_valid_config():
    config = UDPConfig(port=42069, interval=5, address="192.168.1.1")
    assert config.port == 42069
    assert config.interval == 5
    assert config.address == "192.168.1.1"


def test_invalid_port_too_low():
    with pytest.raises(ValueError) as excinfo:
        UDPConfig(port=0, interval=5, address="192.168.1.1")
    assert str(excinfo.value) == "Port must be between 1 and 65535"


def test_invalid_port_too_high():
    with pytest.raises(ValueError) as excinfo:
        UDPConfig(port=65536, interval=5, address="192.168.1.1")
    assert str(excinfo.value) == "Port must be between 1 and 65535"


def test_invalid_interval_too_low():
    with pytest.raises(ValueError) as excinfo:
        UDPConfig(port=42069, interval=0, address="192.168.1.1")
    assert str(excinfo.value) == "Interval must be greater than 0"


def test_invalid_ip_address():
    with pytest.raises(ValueError) as excinfo:
        UDPConfig(port=42069, interval=5, address="invalid_address")
    assert str(excinfo.value) == "Invalid IP address"


if __name__ == "__main__":
    pytest.main()

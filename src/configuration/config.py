import configparser
from collections import namedtuple

from src.configuration.sections import UDPConfig, TCPConfig, HTTPConfig, OtherConfig


class Config:
    """
    Represents a configuration object that loads and manages configuration data from a INI file.

    Attributes:
        file_name (str): The path to the configuration file.
        config (configparser.ConfigParser): The parsed configuration data.
        udp (UDPConfig): The parsed configuration data for the UDP section.
    """

    SECTIONS = ["UDP", "TCP", "HTTP", "OTHER"]

    def __init__(self, file_name: str = "config.ini"):
        """
        Initializes a Config object.

        Args:
            file_name (str, optional): The path to the configuration file. Defaults to "config.ini".

        Raises:
            ValueError: If file_name is not provided.
            FileNotFoundError: If the specified configuration file is not found.
            configparser.MissingSectionHeaderError: If a required section is missing in the configuration file.
        """
        if not file_name:
            raise ValueError("File name is required")

        self.file_name = file_name
        self.template = namedtuple("Config", self.SECTIONS)

        try:
            self.config = self.load()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Configuration file not found: {file_name}!"
                f"Try to create a new one based on instructions in documentation"
            )

        self.udp = self.__load_udp()
        self.tcp = self.__load_tcp()
        self.http = self.__load_http()
        self.other = self.__load_other()

    def load(self) -> configparser.ConfigParser:
        """
        Loads the configuration data from the specified file.

        Returns:
            configparser.ConfigParser: The parsed configuration data.
        """
        config = configparser.ConfigParser()
        config.read(self.file_name)
        return config

    def __get_section(self, section_name: str, config_class):
        """
        Loads a configuration section from the parsed data.

        Args:
            section_name (str): The name of the section to load.
            config_class: The configuration class to use for loading the section.

        Returns:
            config_class: The loaded configuration data for the specified section.

        Raises:
            configparser.NoSectionError: If the specified section is not found in the configuration file.
        """
        try:
            return config_class(
                **{key: self.config.get(section_name, key) for key in self.config[section_name]}
            )
        except configparser.NoSectionError as e:
            raise configparser.NoSectionError(f"Section '{section_name}' not found in configuration file") from e

    def __load_udp(self):
        return self.__get_section("UDP", UDPConfig)

    def __load_tcp(self):
        return self.__get_section("TCP", TCPConfig)

    def __load_http(self):
        return self.__get_section("HTTP", HTTPConfig)

    def __load_other(self):
        return self.__get_section("OTHER", OtherConfig)

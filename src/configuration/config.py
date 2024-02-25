from src.configuration.sections import UDPConfig, TCPConfig, HTTPConfig, OtherConfig
import configparser


class Config:
    """
    Reads and manages configuration settings from a file.

    Attributes:
        config_file_path (str): The path to the configuration file.
        config (configparser.ConfigParser): The parsed configuration data.
        udp_settings (UDPConfig): The UDP-specific settings.
        tcp_settings (TCPConfig): The TCP-specific settings.
        http_settings (HTTPConfig): The HTTP-specific settings.
        other_settings (OtherConfig): The other configuration settings.

    Raises:
        configparser.Error: If there is an error parsing the configuration file.
        FileNotFoundError: If the configuration file is not found.
        ValueError: If there is an error converting values to the correct types.
    """

    def __init__(self, config_file_path: str):
        """
        Initializes the Config object.

        Args:
            config_file_path (str): The path to the configuration file.
        """

        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.load_settings()

    def load_settings(self):
        """
        Reads and parses the configuration file.

        Raises:
            configparser.Error: If there is an error parsing the configuration file.
            FileNotFoundError: If the configuration file is not found.
            ValueError: If there is an error converting values to the correct types.
        """

        try:
            self.config.read(self.config_file_path)

            # Load UDP settings
            udp_config_values = {
                'port': int(self.config["UDP"]["port"]),
                'interval': int(self.config["UDP"]["interval"]),
                'address': self.config["UDP"]["address"]
            }
            self.udp_settings = UDPConfig(**udp_config_values)

            # Load TCP settings
            tcp_config_values = {
                'port': int(self.config["TCP"]["port"]),
                'timeout': int(self.config["TCP"]["timeout"])
            }
            self.tcp_settings = TCPConfig(**tcp_config_values)

            # Load HTTP settings
            http_config_values = {
                'api_port': int(self.config["HTTP"]["port"])
            }
            self.http_settings = HTTPConfig(**http_config_values)

            # Load other settings
            other_config_values = {
                'peer_id': self.config["OTHER"]["peer_id"],
                'max_messages': int(self.config["OTHER"]["max_messages"])
            }
            self.other_settings = OtherConfig(**other_config_values)

        except (configparser.Error, FileNotFoundError, ValueError) as e:
            print(f"Error loading settings: {e}")
            # Handle error gracefully (e.g., create default settings)

    def save_settings(self):
        """
        Saves the configuration settings to the file.
        """

        with open(self.config_file_path, "w") as f:
            self.config.write(f)

    def update_setting(self, section: str, key: str, value):
        """
        Updates a configuration setting in the file
        """

        self.config[section][key] = value
        self.save_settings()

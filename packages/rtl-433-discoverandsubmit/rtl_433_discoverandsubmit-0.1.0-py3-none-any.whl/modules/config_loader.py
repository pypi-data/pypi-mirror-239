import json
import os
import pkg_resources

config_path = pkg_resources.resource_filename('rtl_433_discoverandsubmit', 'config/cli_config.json')


# Define Configuration Paths
CLI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/cli_config.json')
DEVICE_MAPPINGS_PATH = os.path.join(os.path.dirname(__file__), '../config/device_mappings.json')

def load_config(filename):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def get_mqtt_config():
    """Fetch MQTT configuration."""
    return load_config(config_path).get('mqtt', {})


def load_device_mappings(file_path="config/device_mappings.json"):
    """
    Load device mappings from a JSON file.

    :param file_path: Path to the JSON file containing the device mappings.
    :return: Loaded device mappings.
    """
    with open(config_path, "rb") as file:
        return json.load(file)

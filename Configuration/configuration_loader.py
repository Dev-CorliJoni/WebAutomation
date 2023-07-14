import os
from Configuration import Configuration, ConfigurationChecker


def get_configuration(path):
    """
    Loads a configuration from a JSON file.

    :param path: Path to the JSON file.
    :return: Configuration object representing the loaded configuration.
    """
    abs_path = os.path.abspath(path)

    with open(abs_path, 'r') as f, open(r".\Configuration\configuration-schema.json", 'r') as schema:
        json_data = ConfigurationChecker.validate_file(f, schema)

        return Configuration(**json_data)

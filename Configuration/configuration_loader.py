import os
import json
from Configuration import Configuration, ConfigurationChecker


def get_configuration(path):
    abs_path = os.path.abspath(path)

    with open(abs_path, 'r') as f:
        return Configuration(**json.load(f))

import json
from Configuration import Configuration, ConfigurationChecker


def get_configuration(filename):
    with open(filename, 'r') as f:
        return Configuration(**json.load(f))

import json
import jsonschema

from logging_helper import get_logger

logger = get_logger(__name__)


class ConfigurationChecker:

    def __init__(self, schema_file):
        """    
        :param schema_path: The path to the JSON schema file.
        """
        self.schema = json.load(schema_file)

    def validate(self, json_data):
        """
        Validates the given JSON data against a JSON schema.
    
        :param json_data: The JSON data to validate.
        :return: True if the JSON data is valid according to the schema, False otherwise.
        """
        try:
            jsonschema.validate(instance=json_data, schema=self.schema)
            return True
        except Exception as e:
            logger.warning(f"JSON validation error: {str(e)}")
            return False

    @staticmethod
    def validate_file(file, schema_file):
        json_data = json.load(file)
        ConfigurationChecker(schema_file).validate(json_data)
        return json_data

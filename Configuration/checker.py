import json
import jsonschema


class ConfigurationChecker:

    def __init__(self, schema_path):
        """    
        :param schema_path: The path to the JSON schema file.
        """
        self.schema = json.load(schema_path)

    def validate(self, json_data):
        """
        Validates the given JSON data against a JSON schema.
    
        :param json_data: The JSON data to validate.
        :return: True if the JSON data is valid according to the schema, False otherwise.
        """
        try:
            jsonschema.validate(json_data, self.schema)
            return True
        except Exception as e:
            print(f"JSON validation error: {str(e)}")
            return False

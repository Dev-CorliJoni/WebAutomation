import os


class BaseAutomationStep:

    @staticmethod
    def validate_filepath(path):
        if not os.path.isfile(path):
            raise Exception(f"Path is invalid '{path}'!")
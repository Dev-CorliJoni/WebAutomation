import os


class BaseAutomationStep:
    """
    Base class for automation steps.
    """

    @staticmethod
    def validate_filepath(path):
        """
        Validates if the given path is a valid file.

        :param path: The path to validate.
        """
        if not os.path.isfile(path):
            raise Exception(f"Path is invalid '{path}'!")

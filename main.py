import os

from Configuration import get_configuration
from Automation import Automation

"""


class AutomationStepAbbriviationExample:

    def __init__(self, automation_step_data):
        self.data = automation_step_data

    def run(self):
        pass  # do stuff
"""


def config_generator():
    """
    This method collects every json file in the current working directory
    and returns the loaded json documents
    :return: Loaded json documents
    """
    cwd = os.getcwd()
    for filename in filter(lambda file: file.endswith('.json'), os.listdir(cwd)):
        yield get_configuration(os.path.join(cwd, filename))


def main():

    for configuration in config_generator():
        if hasattr(configuration, "webpage"):
            automation = Automation(configuration)
            automation.open_webpage()
            automation.run()


if __name__ == '__main__':
    main()

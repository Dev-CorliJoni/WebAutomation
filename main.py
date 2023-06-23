import os

from helper import get_logger
from Configuration import get_configuration
from Automation import Automation


logger = get_logger(__name__)


def config_generator():
    """
    This method collects every json file in the current working directory
    and returns the loaded json documents
    :return: Loaded json documents
    """
    cwd = os.getcwd()
    for filename in filter(lambda file: file.endswith('.json'), os.listdir(cwd)):
        yield filename, get_configuration(os.path.join(cwd, filename))



def main():
    for filename, configuration in config_generator():
        logger.info(f"Configuration('{filename}') is loaded properly.")
        if hasattr(configuration, "use_config") and getattr(configuration, "use_config") is True:
            automation = Automation(configuration, filename)
            try:
                automation.open_hyperlink()
                automation.run()
            except Exception as e:
                logger.critical(f'Automation failed!\n{automation.get_process_information()}', exc_info=True)
                automation.close()
                raise e


if __name__ == '__main__':
    main()

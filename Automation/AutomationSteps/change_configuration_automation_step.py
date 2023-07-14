from Automation.AutomationSteps.base_automation_step import BaseAutomationStep
from Configuration import get_configuration
from logging_helper import get_logger

logger = get_logger(__name__)


class ChangeConfigurationAutomationStep(BaseAutomationStep):
    """
    Class representing an automation step to change the configuration.
    """

    def __init__(self, automation_step_data):
        """
        Initialize the ChangeConfigurationAutomationStep object.

        :param automation_step_data: The data for the automation step.
        """
        self.configuration = automation_step_data.change_configuration
        self.validate_filepath(self.configuration)

    def __call__(self, *args, **kwargs):
        """
        Execute the change configuration step.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        automation, session = args
        configuration = get_configuration(self.configuration)

        logger.info(f"[ChangeConfigurationAutomationStep] Change to configuration {self.configuration} is initialized.")

        automation.tracker.configuration_path = self.configuration
        automation.configuration = configuration

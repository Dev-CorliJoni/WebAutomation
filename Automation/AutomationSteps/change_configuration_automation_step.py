import os

from Configuration import get_configuration
from logging_helper import  get_logger

logger = get_logger(__name__)

class ChangeConfigurationAutomationStep:
    def __init__(self, automation_step_data):
        self.configuration = automation_step_data.change_configuration

    def __call__(self, *args, **kwargs):
        automation, session = args
        configuration = get_configuration(self.configuration)

        logger.info(f"[ChangeConfigurationAutomationStep] Change to configuration {self.configuration} is initialized.")

        automation.tracker.configuration_path = self.configuration
        automation.configuration = configuration


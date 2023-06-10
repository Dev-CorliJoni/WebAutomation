from Configuration import get_configuration
from Automation.AutomationSteps import BaseStep


class ChangeConfigurationAutomationStep(BaseStep):
    def __init__(self, automation_step_data):
        self.configuration = automation_step_data.change_configuration

    def __call__(self, *args, **kwargs):
        automation, session = super().__call__(*args, **kwargs)
        configuration = get_configuration(self.configuration)
        automation.configuration = configuration


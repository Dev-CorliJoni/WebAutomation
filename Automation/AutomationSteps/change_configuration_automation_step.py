from Configuration import get_configuration


class ChangeConfigurationAutomationStep:
    def __init__(self, automation_step_data):
        self.configuration = automation_step_data.change_configuration

    def __call__(self, *args, **kwargs):
        automation, session = args
        configuration = get_configuration(self.configuration)

        automation.tracker.configuration_path = self.configuration
        automation.configuration = configuration


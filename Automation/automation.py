from logging_helper import get_logger
from Session import Session
from Automation.AutomationSteps import *
from Automation.helper import _has_attributes
from Automation.automation_tracker import AutomationTracker
from WebInterface import WebInterface


logger = get_logger(__name__)


class Automation:

    def __init__(self, configuration, configuration_path):
        self.hyperlink = None
        self._configuration = configuration

        self.web_interface = WebInterface()
        self._session = Session(self.web_interface)
        self.tracker = AutomationTracker(configuration_path, additional_information=True)

        if hasattr(configuration, "hyperlink"):
            self.hyperlink = configuration.hyperlink

    def close(self):
        self.web_interface.close()

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        self._configuration = configuration

        if hasattr(self._configuration, "hyperlink"):
            self.hyperlink = self._configuration.hyperlink
            self.open_hyperlink()
        else:
            # Switch to the last window handle, because maybe the button was clicked and the page redirected
            self.web_interface.switch_to_last_window_handle()
            self._load_configuration()

    def _load_configuration(self):
        self.tracker.changed_configuration(self.hyperlink)
        self._session.update_configuration(self.configuration.controls, self.configuration.control_collections)
        self._steps = [Automation._get_automation_step(data) for data in self.configuration.automation]
        logger.info(f"Configuration('{self.tracker.configuration_filename}') is loaded properly.")

    @staticmethod
    def _get_automation_step(automation_step_data):
        # evaluate type
        if _has_attributes(automation_step_data, "script"):
            return ScriptAutomationStep(automation_step_data)
        elif _has_attributes(automation_step_data, "change_configuration"):
            return ChangeConfigurationAutomationStep(automation_step_data)
        elif _has_attributes(automation_step_data, "element", "action"):
            return ElementAutomationStep(automation_step_data)
        elif _has_attributes(automation_step_data, "elements", "selector", "action"):
            return ElementCollectionAutomationStep(automation_step_data)
        else:
            raise Exception(f"Automation Step could not be parsed: {automation_step_data}")

    def open_hyperlink(self):
        self.web_interface.open(self.hyperlink)
        self._load_configuration()

    def run(self):
        while len(self._steps) > 0:
            self.tracker.step_successful()
            self._steps.pop(0)(self, self._session)

    def get_process_information(self):
        return str(self.tracker)

from logging_helper import get_logger
from Session import Session
from Automation.AutomationSteps import *
from Automation.helper import _has_attributes
from Automation.automation_tracker import AutomationTracker
from WebInterface import WebInterface

logger = get_logger(__name__)


class Automation:
    """
    Class representing the automation process.
    """

    def __init__(self, configuration, configuration_path):
        """
        Initialize the Automation object.

        :param configuration: The configuration object.
        :param configuration_path: The path to the configuration file.
        """
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
        """
        Set the configuration object and update the automation process accordingly.

        :param configuration: The new configuration object.
        """
        self._configuration = configuration

        if hasattr(self._configuration, "hyperlink"):
            self.hyperlink = self._configuration.hyperlink
            self.open_hyperlink()
        else:
            # Switch to the last window handle, because maybe a button was clicked and the page redirected
            self.web_interface.switch_to_last_window_handle()
            self._load_configuration()

    def _load_configuration(self):
        """
        Loads the instructions of configuration and updates the session and steps accordingly.
        """
        self.tracker.changed_configuration(self.hyperlink)
        self._session.update_configuration(self.configuration.controls, self.configuration.control_collections)
        self._steps = [Automation._get_automation_step(data) for data in self.configuration.automation]
        logger.info(f"Configuration('{self.tracker.configuration_filename}') is loaded properly.")

    @staticmethod
    def _get_automation_step(automation_step_data):
        """
        Get the appropriate automation step based on the provided data.

        :param automation_step_data: The data for the automation step.
        :return: The automation step object.
        :raises Exception: If the automation step cannot be parsed.
        """
        automation_steps = (
            (_has_attributes(automation_step_data, "script"), ScriptAutomationStep),
            (_has_attributes(automation_step_data, "change_configuration"), ChangeConfigurationAutomationStep),
            (_has_attributes(automation_step_data, "input"), InputAutomationStep),
            (_has_attributes(automation_step_data, "element", "action"), ElementAutomationStep),
            (_has_attributes(automation_step_data, "elements", "selector", "action"), ElementCollectionAutomationStep)
        )

        try:
            return [automation_step for has_attr, automation_step in automation_steps if has_attr][0](automation_step_data)
        except Exception as e:
            raise Exception(f"Automation Step could not be parsed: {automation_step_data}", e)

        #if _has_attributes(automation_step_data, "script"):
        #    return ScriptAutomationStep(automation_step_data)
        #elif _has_attributes(automation_step_data, "change_configuration"):
        #    return ChangeConfigurationAutomationStep(automation_step_data)
        #elif _has_attributes(automation_step_data, "input"):
        #    return InputAutomationStep(automation_step_data)
        #elif _has_attributes(automation_step_data, "element", "action"):
        #    return ElementAutomationStep(automation_step_data)
        #elif _has_attributes(automation_step_data, "elements", "selector", "action"):
        #    return ElementCollectionAutomationStep(automation_step_data)
        #else:
        #

    def open_hyperlink(self):
        """
        Open the hyperlink in the web interface and load the configuration.
        """
        self.web_interface.open(self.hyperlink)
        self._load_configuration()

    def run(self):
        """
        Run the automation process.
        """
        while len(self._steps) > 0:
            self.tracker.step_successful()
            self._steps.pop(0)(self, self._session)

    def get_process_information(self):
        """
        Get the process information.

        :return: The process information as a string.
        """
        return str(self.tracker)

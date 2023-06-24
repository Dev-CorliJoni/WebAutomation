from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from logging_helper import get_logger
from Session import Session
from Automation.AutomationSteps import *
from Automation.helper import _has_attributes
from Automation.automation_tracker import AutomationTracker


def _get_options():
    options = Options()
    options.add_experimental_option("detach", True)
    return options

logger = get_logger(__name__)

class Automation:

    def __init__(self, configuration, configuration_path):
        self.tracker = AutomationTracker(configuration_path, debug_mode=True) #setto false

        self._configuration = configuration
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=_get_options())
        self._driver.maximize_window()

        self._wait = WebDriverWait(self._driver, 10)
        self._session = Session(self._driver, self._wait)
        self.hyperlink = None

        if hasattr(configuration, "hyperlink"):
            self.hyperlink = configuration.hyperlink

    def close(self):
        self._driver.close()

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
            # Switch to latest window handle, in case Button was clicked and redirected the page
            self._driver.switch_to.window(self._driver.window_handles[-1])
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
        elif _has_attributes(automation_step_data, "element"):
            return ElementAutomationStep(automation_step_data)
        elif _has_attributes(automation_step_data, "elements"):
            return ElementCollectionAutomationStep(automation_step_data)
        else:
            raise Exception(f"Automation Step could not be parsed: {automation_step_data}")

    def open_hyperlink(self):
        if self.hyperlink is not None:
            self._driver.get(self.hyperlink)
        self._driver.switch_to.window(self._driver.window_handles[-1])

        self._load_configuration()

    def run(self):
        while len(self._steps) > 0:
            self.tracker.step_successful()
            self._steps.pop(0)(self, self._session)

    def get_process_information(self):
        return str(self.tracker)

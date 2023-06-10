from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Session import Session
from Automation.helper import _has_attributes
from Automation.AutomationSteps import *

from selenium.webdriver.support.ui import WebDriverWait


def _get_options():
    options = Options()
    options.add_experimental_option("detach", True)
    return options


class BaseAutomation:

    def __init__(self, configuration, driver):
        self._configuration = configuration
        self._driver = driver

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        self._configuration = configuration
        self._load_configuration()

    def _load_configuration(self):
        self._session.update_configuration(self.configuration.controls, self.configuration.control_collections)
        self._steps = [Automation._get_automation_step(data) for data in self.configuration.automation]

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

    def run(self):
        while len(self._steps) > 0:
            self._steps.pop(0)(self, self._session)


class Automation(BaseAutomation):

    def __init__(self, configuration):
        super().__init__(configuration, webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=_get_options()))
        self.link = configuration.webpage
        self._wait = WebDriverWait(self._driver, 20)
        self._session = Session(self._driver, self._wait)

    def open_webpage(self):
        self._driver.get(self.link)
        self._driver.maximize_window()

        self._load_configuration()

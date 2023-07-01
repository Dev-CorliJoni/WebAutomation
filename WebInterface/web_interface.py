from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import ElementNotInteractableException as _ElementNotInteractableException

class WebInterface:

    ElementNotInteractableException = _ElementNotInteractableException

    def __init__(self):
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=WebInterface._get_webdriver_options())
        self._driver.maximize_window()
        self._driver.implicitly_wait(10)

        self._wait = WebDriverWait(self._driver, 10)

    @property
    def wait(self):
        return self._wait

    @property
    def driver(self):
        return self._driver

    def close(self):
        self._driver.close()

    def switch_to_last_window_handle(self):
        self._driver.switch_to.window(self._driver.window_handles[-1])

    def open(self, hyperlink):
        if hyperlink is not None:
            self._driver.get(hyperlink)
        self.switch_to_last_window_handle()

    @staticmethod
    def _get_webdriver_options():
        options = Options()
        options.add_experimental_option("detach", True)
        return options

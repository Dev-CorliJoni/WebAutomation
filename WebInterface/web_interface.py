from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import ElementNotInteractableException as _ElementNotInteractableException


class WebInterface:
    """
    A interface for Selenium WebDriver functionality.
    """

    # Alias for the ElementNotInteractableException class from Selenium.
    ElementNotInteractableException = _ElementNotInteractableException

    def __init__(self):
        """
        Initializes the WebInterface class.
        - Creates a Chrome WebDriver instance using ChromeDriverManager.
        - Maximizes the window and sets an implicit wait of 10 seconds.
        - Initializes WebDriverWait with a timeout of 10 seconds.
        """
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
        """
        Closes the Chrome WebDriver instance.
        """
        self._driver.close()

    def switch_to_last_window_handle(self):
        """
        Switches the focus to the last opened window handle.
        """
        self._driver.switch_to.window(self._driver.window_handles[-1])

    def open(self, hyperlink):
        """
        Opens a URL in the Chrome WebDriver.
        - If a hyperlink is provided, navigates to the specified URL.
        - Switches the focus to the last opened window handle.
        """
        if hyperlink is not None:
            self._driver.get(hyperlink)
        self.switch_to_last_window_handle()

    @staticmethod
    def _get_webdriver_options():
        """
        Returns Chrome WebDriver options with "detach" option enabled.
        """
        options = Options()
        options.add_experimental_option("detach", True)
        return options

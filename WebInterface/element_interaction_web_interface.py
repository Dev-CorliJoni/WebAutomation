import requests
from PIL import Image
from io import BytesIO

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from logging_helper import get_logger

logger = get_logger(__name__)


def _access_control(control, function):
    """
    If the passed control is enabled, the specified function will be executed.
    """
    if control.is_enabled():
        return function()
    else:
        raise Exception("[ElementNotEnabled]")

class ElementInteractionWebInterface:
    """
    A class that provides functionality for interacting with HTML elements.
    """

    KEYS = Keys

    @staticmethod
    def resolve(web_interface, xpath):
        """
        Resolves a single HTML element using the provided XPath.

        :param web_interface:
        :param xpath: The xpath of the HTML element
        """
        try:
            web_interface.wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return web_interface.driver.find_element("xpath", xpath)
        except Exception as e:
            logger.exception(f"The element with x-path='{xpath}' could not be found!", e)

    @staticmethod
    def resolve_many(web_interface, xpath):
        """
        Resolves multiple HTML elements using the provided XPath.

        :param web_interface:
        :param xpath: The xpath of the HTML element
        """
        try:
            web_interface.wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
            return web_interface.driver.find_elements("xpath", xpath)
        except TimeoutException:
            logger.error(f"Timeout: The requested element with x-path='{xpath} could not be found! "
                         f"If not necessary, remove this request for performance!")
            return []
        except Exception as e:
            logger.exception(f"The element(s) with x-path='{xpath}' could not be found!", e)

    @staticmethod
    def click(session, control, **kwargs):
        """
        Performs a click action on the specified control if it is enabled.
        """
        _access_control(control, lambda: control.click())

    @staticmethod
    def read(session, control, **kwargs):
        """
        Reads the text content of the specified control and stores it in the provided variable.
        - If the control's text is empty, finds the first sub-element with non-empty text and uses it instead.
        - If the variable is a list, appends the text to the list.
        - Otherwise, sets the variable to the text.
        """
        variable = kwargs["variable"]
        value = ElementInteractionWebInterface.get_content(session, control, type_="text")

        if hasattr(session.data, variable) and type(getattr(session.data, variable)) is list:
            getattr(session.data, variable).append(value)
        else:
            setattr(session.data, variable, value)

    @staticmethod
    def write(session, control, **kwargs):
        """
        Sends the resolved value to the control.
        """
        values = kwargs["values"]

        for value in values:
            _access_control(control, lambda: control.send_keys(value))

    @staticmethod
    def get_content(session, control, type_=None):
        """
        Gets the content of the control.
        """
        text = _access_control(control, lambda :control.text)
        source = _access_control(control, lambda :control.get_attribute("src"))

        if source is not None and type_ in ("img", None):
            return Image.open(requests.get(source, stream=True).raw)

        elif type_ in ("text", None):
            c = control

            if text == "":
                sub_element_with_text_xpath = "//*[not(text()='')]"
                session.web_interface.wait.until(ec.presence_of_all_elements_located((By.XPATH, sub_element_with_text_xpath)))
                c = control.find_element(By.XPATH, sub_element_with_text_xpath)

            return _access_control(c, lambda :c.text)

        elif type_ in ("screenshot",):
            screenshot_bytes = _access_control(control, lambda: control.screenshot_as_png)
            return Image.open(BytesIO(screenshot_bytes))

        elif type_ in ("html",):
            return _access_control(control, lambda: control.get_attribute("innerHTML"))

        elif type_ in ("pdf",):
            pass

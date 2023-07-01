from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from logging_helper import get_logger
from WebInterface.helper.string_replacer import StringReplacer


logger = get_logger(__name__)


def _access_control(control, function):
    if control.is_enabled():
        function()
    else:
        raise Exception("[ElementNotEnabled]")

class ElementInteractionWebInterface:

    @staticmethod
    def resolve(web_interface, xpath):
        """
        :param web_interface:
        :param xpath: The xpath of the HTML element
        :return: An ... object, that is provide functionality to interact with the HTML element
        """

        try:
            web_interface.wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            return web_interface.driver.find_element("xpath", xpath)
        except Exception as e:
            logger.exception(f"The element with x-path='{xpath}' could not be found!", e)

    @staticmethod
    def resolve_many(web_interface, xpath):
        """
        :param web_interface:
        :param xpath: The xpath of the HTML elements
        :return: An ... object, that is provide functionality to interact with the HTML element
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
        _access_control(control, lambda: control.click())

    @staticmethod
    def read(session, control, **kwargs):
        variable = kwargs["variable"]
        c = control

        if control.text == "":
            sub_element_with_text_xpath = "//*[not(text()='')]"
            session.wait.until(ec.presence_of_all_elements_located((By.XPATH, sub_element_with_text_xpath)))
            c = control.find_element(By.XPATH, sub_element_with_text_xpath)

        if hasattr(session.data, variable) and type(getattr(session.data, variable)) is list:
            _access_control(c, lambda: getattr(session.data, variable).append(c.text))
        else:
            _access_control(c, lambda: setattr(session.data, variable, c.text))

    @staticmethod
    def write(session, control, **kwargs):
        value = kwargs["value"]

        value = StringReplacer.resolve_variables(value, session.data)
        values = list(StringReplacer.resolve_special_keys(value))

        for value in values:
            _access_control(control, lambda: control.send_keys(value))


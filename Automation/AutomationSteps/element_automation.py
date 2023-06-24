import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


def _access_control(session, control, function, expected_conditions_function=None):
    #if expected_conditions_function is not None:
    #    session.wait.until(expected_conditions_function((By.XPATH, control.id)))
    time.sleep(0.15)

    if control.is_enabled():
        function()
    else:
        raise Exception("[ElementNotEnabled]")


class Actions:
    CLICK = "click"
    READ = "read"
    WRITE = "write"


class ElementAutomation:

    def __init__(self, action, variable, value):
        self.action = action
        self.variable = variable
        self.value = value

        self.action_method = self._get_action()
        self._check_variable_name_validity()

    def _check_variable_name_validity(self):
        if self.variable is not None:
            end_markers_in_name = [end_marker for end_marker in SpecialKeys.END_MARKERS if end_marker in self.variable]
            if len(end_markers_in_name) > 0:
                raise Exception(f"[InvalidVariableName]: Invalid characters in variable name: { ' , '.join(end_markers_in_name)}")

    def _get_action(self):
        actions = {
            Actions.CLICK: self._click,
            Actions.READ: self._read,
            Actions.WRITE: self._write
        }

        if self.action in actions.keys():
            return actions[self.action]
        raise Exception(f"[ActionNotAvailable]: Action {self.action} is not supported")

    def __call__(self, *args, **kwargs):
        control = args[0]
        session = args[1]

        self.action_method(control, session)

    def _click(self, control, session):
        _access_control(session, control, lambda: control.click(), ec.element_to_be_selected)

    def _read(self, control, session):
        c = control

        if control.text == "":
            sub_element_with_text_xpath = "//*[not(text()='')]"
            session.wait.until(ec.presence_of_all_elements_located((By.XPATH, sub_element_with_text_xpath)))
            c = control.find_element(By.XPATH, sub_element_with_text_xpath)

        _access_control(session, c, lambda: setattr(session.data, self.variable, c.text))

    def _write(self, control, session):
        self.value = StringReplacer.resolve_variables(self.value, session.data)
        values = list(StringReplacer.resolve_special_keys(self.value))

        for value in values:
            _access_control(session, control, lambda: control.send_keys(value))


class SpecialKeys:
    SPACE = " "
    OPEN_SQUARE_BRACKET = "["
    CLOSING_SQUARE_BRACKET = "]"
    DOLLAR = "$"

    ADDITIONAL_END_MARKERS = ["?", "!", "^", "°", "@", "€", "*", "+", "~", "#", "'", "-", ".", ",", ";", ":", "<", ">", "|", "\"",
                              "§", "%", "&", "/", "{", "(", ")", "[", "]", "}", "=", "\\", "´", "`"]

    START_MARKERS = [OPEN_SQUARE_BRACKET, DOLLAR]
    END_MARKERS = [OPEN_SQUARE_BRACKET, CLOSING_SQUARE_BRACKET, SPACE, DOLLAR]
    END_MARKERS.extend(ADDITIONAL_END_MARKERS)


class StringReplacer:

    @staticmethod
    def resolve_variables(value, data):

        return_value = ""

        for variable_name in StringReplacer.get_elements_by_markers(value, SpecialKeys.DOLLAR, SpecialKeys.END_MARKERS, False):

            if hasattr(data, variable_name):
                variable_content = getattr(data, variable_name)
            else:
                raise Exception(f"[VariableNotAvailable]: Variable ${variable_name} is not available")

            # value[:value.find(variable_name) - 1] -> The -1 removes $
            return_value = f"{return_value}{value[:value.find(variable_name) - 1]}{variable_content}"
            value = value[value.find(variable_name) + len(variable_name):]

        return f"{return_value}{value}"

    @staticmethod
    def resolve_special_keys(value):
        elements = StringReplacer.get_elements_by_markers(value, SpecialKeys.OPEN_SQUARE_BRACKET, [SpecialKeys.CLOSING_SQUARE_BRACKET])

        for variable_name in elements:

            if hasattr(Keys, variable_name):
                variable_content = getattr(Keys, variable_name)
            else:
                raise Exception(f"[KeyNotAvailable]: Key [{variable_name}] is not available")

            # value[:value.find(variable_name) - 1] -> The -1 removes $
            yield value[:value.find(variable_name) - 1]
            yield variable_content

            value = value[value.find(variable_name) + len(variable_name) + 1:]

        if value != "":
            yield value

    @staticmethod
    def get_elements_by_markers(value: str, start_marker: str, end_markers: str, is_end_marker_necessary=True):
        start_index = value.find(start_marker)
        end_index = StringReplacer._get_end_index(value, end_markers, start_index)

        while start_marker in value and (StringReplacer._are_end_markers_in_value(value, end_markers, start_index) or not is_end_marker_necessary):
            yield value[start_index + 1:end_index]

            if value[end_index] == "]":
                end_index = end_index + 1

            value = value[end_index:len(value)]

            start_index = value.find(start_marker)
            end_index = StringReplacer._get_end_index(value, end_markers, start_index)

    @staticmethod
    def _get_end_index(value, end_markers, start_index):
        end_marker_indexes = [value.find(end_marker, start_index + 1) for end_marker in end_markers if end_marker in value[start_index+1:]]
        return min(end_marker_indexes, default=len(value))

    @staticmethod
    def _are_end_markers_in_value(value, end_markers, start_index):
        return any([end_marker in value[start_index:] for end_marker in end_markers])


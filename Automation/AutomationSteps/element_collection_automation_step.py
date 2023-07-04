import random
from logging_helper import get_logger
from WebInterface import WebInterface
from WebInterface.helper.special_char import SpecialChar
from Automation.helper import _has_attributes
from Automation.AutomationSteps import ElementAutomation, Actions

logger = get_logger(__name__)

def get_message(name, selector, action, variable=None, value=None):
    """
    Generates a descriptive message based on the element names, selector, action, variable, and value.

    :param name: The name of the elements.
    :param selector: The selector used to select elements.
    :param action: The action performed on the elements.
    :param variable: The variable used for read action (optional).
    :param value: The value used for the write action (optional).
    :return: The descriptive message.
    """
    return {
        Actions.CLICK:  f"Clicked on element(s) '{name}' with selector '{selector}'.",
        Actions.READ:   f"Read out content(s) of element(s) '{name}' with selector '{selector}' and saved it in '{variable}'.",
        Actions.WRITE:  f"Wrote '{value}' to element(s) '{name}' with selector '{selector}'."
    }[action]


class Selector:
    FOREACH = "foreach"
    REVERSE_FOREACH = "reverse-foreach"
    RANDOM = "random"


class ElementCollectionAutomationStep:
    """
    Class representing an element collection automation step.
    """

    def __init__(self, automation_step_data):
        """
        Initializes an ElementCollectionAutomationStep instance.

        :param automation_step_data: The data for the automation step.
        """
        self.element_names = automation_step_data.elements
        self.selector = automation_step_data.selector
        self.action = automation_step_data.action
        self.variable = None
        self.value = None

        if _has_attributes(automation_step_data, "variable"):
            self.variable = automation_step_data.variable
        elif _has_attributes(automation_step_data, "value"):
            self.value = automation_step_data.value

    def __call__(self, *args, **kwargs):
        """
        Executes the element collection automation step.

        :param args: Arguments passed to the call.
        :param kwargs: Keyword arguments passed to the call.
        """
        automation, session = args

        elements = self._resolve_elements(session)
        values = self._get_value(session, len(elements))

        if len(elements) > len(values):
            raise Exception(f"[ValueError]: The amount of Values {values} has to be equal, to the amount of elements ({len(elements)})")

        if self.action == Actions.READ:
            setattr(session.data, self.variable, [])

        try:
            run_element_automation = lambda _element, value: ElementAutomation(self.action, self.variable, value)(_element, session)

            if self.selector == Selector.RANDOM:
                # Random selector only uses the first value in self.value list
                run_element_automation(random.choice(elements), values[0])
            elif self.selector == Selector.FOREACH:
                [run_element_automation(element, values[i]) for i, element in enumerate(elements)]
            elif self.selector == Selector.REVERSE_FOREACH:
                [run_element_automation(element, values[i]) for i, element in enumerate(reversed(elements))]
            else:
                raise Exception(f"[SelectorNotAvailable]: Selector {self.selector} is not supported")

            msg = get_message(self.element_names, self.selector, self.action, self.variable, values)
            logger.info(f"[ElementCollectionAutomationStep] {msg}")

        except WebInterface.ElementNotInteractableException:
            self.log_elements_not_available_exception()

        except Exception as e:
            if "[ElementNotEnabled]" in str(e):
                self.log_elements_not_available_exception()
            elif hasattr(e, "msg"):
                raise Exception(f"[ElementAutomationStepFailed] {e.msg}", e)
            else:
                raise Exception(f"[ElementAutomationStepFailed]", e)

    def _resolve_elements(self, session):
        """
        Resolves the elements based on the element names in the session.

        :param session: The session containing the controls and control collections.
        :return: The resolved elements.
        """
        if type(self.element_names) is str:
            elements = session.control_collections[self.element_names]
        elif type(self.element_names) is list:
            elements = [session.controls[name] for name in self.element_names if name in dict(session.controls)]
            c_collections = [session.control_collections[name] for name in self.element_names if name in dict(session.control_collections)]
            elements.extend([control for control_collection in c_collections for control in control_collection])
        else:
            msg = f"Type: {type(self.element_names)} of element_names {self.element_names} is not accepted!"
            raise Exception(f"[UnexpectedElementNamesType]: {msg}")

        return elements

    def _get_value(self, session, elements_count):
        """
        Gets the value to use for the automation step.

        :param session: The session containing the data.
        :param elements_count: The number of elements.
        :return: The value to use.
        """
        if self.is_value_resolvable():
            return getattr(session.data, self.value[1:])
        if type(self.value) is str or self.value is None:
            # The list is multiplied so that the value occurs in it as often as there are elements
            return [self.value] * elements_count
        elif type(self.value) is list:
            return self.value
        else:
            raise Exception(f"[UnexpectedValueType]: Type: {type(self.value)} of Value {self.value} is not accepted!")

    def is_value_resolvable(self):
        """
        Checks if the value is resolvable.

        :return: True if the value is resolvable, False otherwise.
        """
        if self.value is None:
            return False

        is_value_resolvable = type(self.value) is str
        is_value_resolvable = is_value_resolvable and self.value.startswith(SpecialChar.DOLLAR) and len(self.value) > 1
        is_end_marker_inside = any([end_marker in self.value for end_marker in SpecialChar.END_MARKERS if end_marker != SpecialChar.DOLLAR])
        is_value_resolvable = is_value_resolvable and not is_end_marker_inside

        return is_value_resolvable

    def log_elements_not_available_exception(self):
        """
        Logs an exception message for elements that are not available.
        """
        msg = f"The action '{self.action}' on controls with the key '{self.element_names}' could not be executed!"
        logger.error(f"[ElementAutomationStepFailed] {msg}")

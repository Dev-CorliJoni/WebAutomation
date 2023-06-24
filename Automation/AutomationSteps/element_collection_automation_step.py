import random

from selenium.common import ElementNotInteractableException

from logging_helper import get_logger
from Automation.helper import _has_attributes
from Automation.AutomationSteps import ElementAutomation, Actions

logger = get_logger(__name__)


def get_message(name, selector, action, variable=None, value=None):
    return {
        Actions.CLICK:  f"Clicked on element(s) '{name}' with selector '{selector}'.",
        Actions.READ:   f"Read out content(s) of element(s) '{name}' with selector '{selector}' and saved it in '{variable}'.",
        Actions.WRITE:  f"Wrote '{value}' to element(s) '{name}' with selector '{selector}'."
    }[action]


class ElementCollectionAutomationStep:
    def __init__(self, automation_step_data):
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
        automation, session = args

        elements = self._resolve_elements(session)
        values = self._get_value(len(elements))

        try:
            run_element_automation = lambda _element, value: ElementAutomation(self.action, self.variable, value)(_element, session)

            if self.selector == "random":
                # Random selector only uses the first value in self.value list
                run_element_automation(random.choice(elements), values[0])
            elif self.selector == "foreach":
                [run_element_automation(element, values[i]) for i, element in enumerate(elements)]
            elif self.selector == "reverse-foreach":
                [run_element_automation(element, values[i]) for i, element in enumerate(reversed(elements))]
            else:
                raise Exception(f"[SelectorNotAvailable]: Selector {self.selector} is not supported")

            msg = get_message(self.element_names, self.selector, self.action, self.variable, values)
            logger.info(f"[ElementCollectionAutomationStep] {msg}")

        except ElementNotInteractableException:
            self.log_elements_not_available_exception()

        except Exception as e:
            if "[ElementNotEnabled]" in str(e):
                self.log_elements_not_available_exception()
            elif hasattr(e, "msg"):
                raise Exception(f"[ElementAutomationStepFailed] {e.msg}", e)
            else:
                raise Exception(f"[ElementAutomationStepFailed]", e)

    def _resolve_elements(self, session):
        # Resolve xpaths to objects
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

    def _get_value(self, elements_count):
        if type(self.value) is str or self.value is None:
            # The list is multiplied so that the value occurs in it as often as there are elements
            return [self.value] * elements_count
        elif type(self.value) is list:
            return self.value
        else:
            raise Exception(f"[UnexpectedValueType]: Type: {type(self.value)} of Value {self.value} is not accepted!")

    def log_elements_not_available_exception(self):
        msg = f"The action '{self.action}' on controls with the key '{self.element_names}' could not be executed!"
        logger.error(f"[ElementAutomationStepFailed] {msg}")
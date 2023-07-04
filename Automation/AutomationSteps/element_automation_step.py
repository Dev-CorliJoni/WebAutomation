from logging_helper import get_logger
from Automation.helper import _has_attributes
from Automation.AutomationSteps import ElementAutomation, Actions

logger = get_logger(__name__)


def get_message(name, action, variable=None, value=None):
    """
    Generates a descriptive message based on the element name, action, variable, and value.

    :param name: The name of the element.
    :param action: The action performed on the element.
    :param variable: The variable associated with the element (optional).
    :param value: The value used for the write action (optional).
    :return: The descriptive message.
    """
    return {
        Actions.CLICK: f"Clicked on element {name}.",
        Actions.READ: f"Read out content of element {name} and saved it in {variable}.",
        Actions.WRITE: f"Wrote '{value}' to element {name}."
    }[action]


class ElementAutomationStep:
    """
    Class representing an element automation step.
    """

    def __init__(self, automation_step_data):
        """
        Initializes an ElementAutomationStep instance.

        :param automation_step_data: The data for the automation step.
        """
        self.element_name = automation_step_data.element
        self.action = automation_step_data.action
        self.variable = None
        self.value = None

        if _has_attributes(automation_step_data, "variable"):
            self.variable = automation_step_data.variable
        elif _has_attributes(automation_step_data, "value"):
            self.value = automation_step_data.value

        self.element_automation = ElementAutomation(self.action, self.variable, self.value)

    def __call__(self, *args, **kwargs):
        """
        Executes the element automation step.

        :param args: Arguments passed to the call.
        :param kwargs: Keyword arguments passed to the call.
        """
        _, session = args
        control = session.controls[self.element_name]

        try:
            self.element_automation(control, session)
            logger.info(f"[ElementAutomationStep] {get_message(self.element_name, self.action, self.variable, self.value)}")
        except Exception as e:
            if "[ElementNotEnabled]" in str(e):
                raise Exception(f"[ElementAutomationStepFailed] Element {self.element_name} is not enabled")
            else:
                raise e

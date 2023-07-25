from Automation.AutomationSteps.helper import print_formatted
from logging_helper import get_logger
from Automation.AutomationSteps.base_automation_step import BaseAutomationStep


logger = get_logger(__name__)


def _get_input(input_):
    if type(input_) is str:
        return [input_]
    elif type(input_) is list:
        return input_
    else:
        return None


class InputAutomationStep(BaseAutomationStep):

    def __init__(self, automation_step_data):
        """
        Initializes a InputAutomationStep instance.

        """
        self.input = _get_input(automation_step_data.input)
        #validate variable names

    def __call__(self, *args, **kwargs):
        """
        Executes the InputAutomationStep.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        automation, session = args
        print_formatted("Request Input", lambda: self.request_input(session.data))

        logger.info(f"[InputAutomationStep] Inputs queried : {self.input}.")

    def request_input(self, data):
        for input_ in self.input:
            setattr(data, input_, input(f"{input_} :"))

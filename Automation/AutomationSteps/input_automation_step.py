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

    def __call__(self, *args, **kwargs):
        """
        Executes the InputAutomationStep.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        automation, session = args

        for input_ in self.input:
            setattr(session.data, input_, input(f"{input_} :"))

        logger.info(f"[InputAutomationStep] Inputs queried : {self.input}.")

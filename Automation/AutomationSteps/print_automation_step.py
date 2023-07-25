from Automation.AutomationSteps.helper import ValueResolver, print_formatted
from logging_helper import get_logger
from Automation.AutomationSteps.base_automation_step import BaseAutomationStep

logger = get_logger(__name__)

class PrintAutomationStep(BaseAutomationStep):
    def __init__(self, automation_step_data):
        """
        Initializes a PrintAutomationStep.

        :param automation_step_data: An object containing automation step data.
        """
        self.print = automation_step_data.print

    def __call__(self, *args, **kwargs):
        """
        Executes the PrintAutomationStep.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        automation, session = args

        print_value = ValueResolver.resolve_variables(self.print, session.data)
        print_formatted("Print Result", lambda: print_value)

        logger.info(f"[PrintAutomationStep] printed:\n{self.print}")

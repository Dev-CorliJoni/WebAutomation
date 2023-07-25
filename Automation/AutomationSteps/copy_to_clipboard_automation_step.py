import os
from PIL import Image

from logging_helper import get_logger
from WebInterface import ElementInteractionWebInterface
from Automation.AutomationSteps.helper import clipboard, ValueResolver
from Automation.AutomationSteps.base_automation_step import BaseAutomationStep


logger = get_logger(__name__)


class CopyToClipboardAutomationStep(BaseAutomationStep):

    def __init__(self, automation_step_data):
        """
        Initializes a CopyToClipboardAutomationStep instance.

        """
        self.copy_to_clipboard = automation_step_data.copy
        self.type = None

        if hasattr(automation_step_data, "type"):
            self.type = automation_step_data.type


    def __call__(self, *args, **kwargs):
        """
        Executes the CopyToClipboardAutomationStep.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        automation, session = args

        if self.copy_to_clipboard in dict(session.controls):
            control = session.controls[self.copy_to_clipboard]
            content = ElementInteractionWebInterface.get_content(session, control, self.type)
        elif os.path.isfile(self.copy_to_clipboard):
            if self.copy_to_clipboard.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                content =  Image.open(self.copy_to_clipboard)
            else:
                with open(self.copy_to_clipboard, "r") as f:
                    content = "".join(f.readlines())
        else:
            content = ValueResolver.resolve_variables(self.copy_to_clipboard, session.data)

        clipboard.copy(content)
        logger.info(f"[CopyToClipboardAutomationStep] copied to clipboard:\n{self.copy_to_clipboard}.")

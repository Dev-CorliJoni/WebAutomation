import os
import sys
import importlib.util

from logging_helper import get_logger
from Automation.AutomationSteps.BaseAutomationStep import BaseAutomationStep


logger = get_logger(__name__)


def import_module(path):
    """
    Dynamically imports a module given a file path.

    :param path: The file path of the module.
    :return: The imported module.
    """
    path = os.path.abspath(path)
    path_parts = path.split('.')[0].split('\\')

    filename = path_parts[-1]

    spec = importlib.util.spec_from_file_location(filename, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[filename] = module
    spec.loader.exec_module(module)
    return module


class ScriptAutomationStep(BaseAutomationStep):
    def __init__(self, automation_step_data):
        """
        Initializes a ScriptAutomationStep instance.

        :param automation_step_data: An object containing automation step data.
        """
        self.script_path = automation_step_data.script
        self.validate_filepath(self.script_path)

    def __call__(self, *args, **kwargs):
        """
        Executes the ScriptAutomationStep.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        """
        automation, session = args

        module = import_module(self.script_path)
        module.run(session)

        logger.info(f"[ScriptAutomationStep] Executed script {self.script_path}.")

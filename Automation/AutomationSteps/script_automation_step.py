import os
import sys
import importlib.util
from logging_helper import get_logger


logger = get_logger(__name__)


def import_module(path):
    path = os.path.abspath(path)
    path_parts = path.split('.')[0].split('\\')

    filename = path_parts[-1]

    spec = importlib.util.spec_from_file_location(filename, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[filename] = module
    spec.loader.exec_module(module)
    return module


class ScriptAutomationStep:
    def __init__(self, automation_step_data):
        self.script_path = automation_step_data.script

    def __call__(self, *args, **kwargs):
        automation, session = args

        module = import_module(self.script_path)
        module.run(session)

        logger.info(f"[ScriptAutomationStep] Executed script {self.script_path}.")

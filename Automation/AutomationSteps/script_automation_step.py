from Automation.AutomationSteps import BaseStep


class ScriptAutomationStep(BaseStep):
    def __init__(self, automation_step_data):
        self.script_path = automation_step_data.script

    def __call__(self, *args, **kwargs):
        _, session = super().__call__(*args, **kwargs)
        script = __import__(f"Scripts")
        getattr(script, self.script_path).run(session)

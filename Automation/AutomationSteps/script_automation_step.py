class ScriptAutomationStep:
    def __init__(self, automation_step_data):
        self.script_path = automation_step_data.script

    def __call__(self, *args, **kwargs):
        automation, session = args
        script = __import__(f"Scripts")
        getattr(script, self.script_path).run(session)

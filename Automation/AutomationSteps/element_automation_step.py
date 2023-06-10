from Automation.helper import _has_attributes
from Automation.AutomationSteps import BaseStep, ElementAutomation


class ElementAutomationStep(BaseStep):
    def __init__(self, automation_step_data):
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
        _, session = super().__call__(*args, **kwargs)
        control = session.controls[self.element_name]

        self.element_automation(control, session)


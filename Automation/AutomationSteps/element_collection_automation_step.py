import random

from Automation.helper import _has_attributes
from Automation.AutomationSteps import BaseStep, ElementAutomation


class ElementCollectionAutomationStep(BaseStep):
    def __init__(self, automation_step_data):
        self.element_names = automation_step_data.elements
        self.selector = automation_step_data.selector
        self.action = automation_step_data.action
        self.variable = None
        self.value = None

        if _has_attributes(automation_step_data, "variable"):
            self.variable = automation_step_data.variable
        elif _has_attributes(automation_step_data, "value"):
            self.value = automation_step_data.value

    def __call__(self, *args, **kwargs):
        automation, session = super().__call__(*args, **kwargs)

        # Resolve xpaths to objects
        if type(self.element_names) is str:
            elements = session.control_collections[self.element_names]
        elif type(self.element_names) is list:
            elements = [session.controls[name] for name in self.element_names if name in dict(session.controls)]
            c_collections = [session.control_collections[name] for name in self.element_names if name in dict(session.control_collections)]
            elements.extend([control for control_collection in c_collections for control in control_collection])

        if type(self.value) is str or self.value is None:
            # The list is multiplied so that the value occurs in it as often as there are elements
            self.value = [self.value] * len(elements)
        elif type(self.value) is list:
            pass
        else:
            raise Exception(f"[UnexpectedValueType]: Type: {type(self.value)} of Value {self.value} is not accepted!")

        if self.selector == "random":
            # Random selector only uses the first value in self.value list
            element = random.choice(elements)
            ElementAutomation(self.action, self.variable, self.value[0])(element, session)
        elif self.selector == "foreach":
            [ElementAutomation(self.action, self.variable, self.value[i])(element, session) for i, element in enumerate(elements)]
        elif self.selector == "reverse-foreach":
            [ElementAutomation(self.action, self.variable, self.value[i])(element, session) for i, element in enumerate(reversed(elements))]

        else:
            raise Exception(f"[SelectorNotAvailable]: Selector {self.selector} is not supported")

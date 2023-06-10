from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class ElementAutomation:

    def __init__(self, action, variable, value):
        self.action = action
        self.variable = variable
        self.value = value

    def __call__(self, *args, **kwargs):
        control = args[0]
        session = args[1]

        if self.action == "click":      # CLICK
            self._click(control, session)
        elif self.action == "read":     # READ
            self._read(control, session)
        elif self.action == "write":    # WRITE
            self._write(control, session)
        else:
            raise Exception(f"[ActionNotAvailable]: Action {self.action} is not supported")

    def _click(self, control, session):
        control.click()

    def _read(self, control, session):
        setattr(session.data, self.variable, control.text)

    def _write(self, control, session):
        if self.value.startswith("$"):
            if hasattr(session.data, self.value[1:]):
                self.value = getattr(session.data, self.value[1:])
            else:
                raise Exception(f"[VariableNotAvailable]: Variable {self.value} is not available")

        control.send_keys(self.value)


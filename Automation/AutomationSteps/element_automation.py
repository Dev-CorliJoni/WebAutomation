from WebInterface import ElementInteractionWebInterface
from WebInterface.helper.special_char import SpecialChar


class Actions:
    CLICK = "click"
    READ = "read"
    WRITE = "write"


class ElementAutomation:

    def __init__(self, action, variable, value):
        self.action = action
        self.variable = variable
        self.value = value

        self.action_method = self._get_action()
        self._check_variable_name_validity()

    def _check_variable_name_validity(self):
        if self.variable is not None:
            end_markers_in_name = [end_marker for end_marker in SpecialChar.END_MARKERS if end_marker in self.variable]
            if len(end_markers_in_name) > 0:
                raise Exception(f"[InvalidVariableName]: Invalid characters in variable name: { ' , '.join(end_markers_in_name)}")

    def _get_action(self):
        actions = {
            Actions.CLICK: ElementInteractionWebInterface.click,
            Actions.READ: ElementInteractionWebInterface.read,
            Actions.WRITE: ElementInteractionWebInterface.write
        }

        if self.action in actions.keys():
            return actions[self.action]
        raise Exception(f"[ActionNotAvailable]: Action {self.action} is not supported")

    def __call__(self, *args, **kwargs):
        control = args[0]
        session = args[1]

        self.action_method(session, control, variable=self.variable, value=self.value)
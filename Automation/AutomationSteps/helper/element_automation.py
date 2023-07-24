from Automation.AutomationSteps.helper.value_resolver import ValueResolver
from WebInterface import ElementInteractionWebInterface
from WebInterface.helper.special_char import SpecialChar


class Actions:
    """
    Class that defines constants for different actions.
    """
    CLICK = "click"
    READ = "read"
    WRITE = "write"


class ElementAutomation:
    """
    Class representing an element automation.
    """

    def __init__(self, action, variable, value):
        """
        Initializes an ElementAutomation instance.

        :param action: The action to perform (click, read, write).
        :param variable: The variable name for read action (optional).
        :param value: The value to use for write action (optional).
        """
        self.action = action
        self.variable = variable
        self.value = value

        self.action_method = self._get_action()
        self._check_variable_name_validity()

    def _check_variable_name_validity(self):
        """
        Checks the validity of the variable name.

        Raises an exception if the variable name contains invalid characters.
        """
        if self.variable is not None:
            end_markers_in_name = [end_marker for end_marker in SpecialChar.END_MARKERS if end_marker in self.variable]
            if len(end_markers_in_name) > 0:
                raise Exception(f"[InvalidVariableName]: Invalid characters in variable name: {', '.join(end_markers_in_name)}")

    def _get_action(self):
        """
        Retrieves the corresponding action method based on the action name.

        :return: The action method.
        """
        actions = {
            Actions.CLICK: ElementInteractionWebInterface.click,
            Actions.READ: ElementInteractionWebInterface.read,
            Actions.WRITE: ElementInteractionWebInterface.write
        }

        if self.action in actions.keys():
            return actions[self.action]
        raise Exception(f"[ActionNotAvailable]: Action {self.action} is not supported")

    def __call__(self, *args, **kwargs):
        """
        Executes the element automation.

        :param args: Arguments passed to the call.
        :param kwargs: Keyword arguments passed to the call.
        """
        control = args[0]
        session = args[1]

        values = ValueResolver.resolve(self.value, session.data, ElementInteractionWebInterface.KEYS)

        self.action_method(session, control, variable=self.variable, values=values)

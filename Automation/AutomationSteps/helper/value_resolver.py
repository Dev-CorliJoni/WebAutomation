import re

class TextPart:
    """
    Represents a part of the input string and its corresponding replacement text.
    """

    def __init__(self, text, replacement=None):
        """
        Initialize a TextPart instance.

        Args:
            text (str): The part of the input string.
            replacement (str, optional): The corresponding replacement text. Defaults to the same as text.
        """
        self.text = text
        if replacement is None:
            self.replacement = text
        else:
            self.replacement = replacement

class EscapedPart(TextPart):
    """
    Represents an escaped part of the input string (e.g., \[, \], \$).
    """

    pass

class VariablePart(TextPart):
    """
    Represents a variable placeholder inside the input string.
    """

    def __init__(self, text, content):
        """
        Initialize a VariablePart instance.

        Args:
            text (str or TextPart): The part of the input string or a TextPart instance.
            content (str): The value of the variable.
        """
        if type(text) is str:
            super().__init__(text, content)
        elif type(text) is TextPart:
            super().__init__(text.text, content)

    @property
    def content(self):
        return self.replacement

class SpecialKeyPart(TextPart):
    """
    Represents a special key part of the input string enclosed in [].
    """

    def __init__(self, text, key):
        """
        Initialize a SpecialKeyPart instance.

        Args:
            text (str or TextPart): The part of the input string or a TextPart instance.
            key (str): The value of the special key.
        """
        if type(text) is str:
            super().__init__(text, key)
        elif type(text) is TextPart:
            super().__init__(text.text, key)

    @property
    def key(self):
        return self.replacement

def _resolve_as_str(escape_method, method, input_str):
    """
    Helper function to resolve input string using the specified method and return the result as a string.

    Args:
        method (function): The resolution method to use.
        input_str (str): The input string to be resolved.

    Returns:
        str: The resolved input string.
    """
    results = list(escape_method([TextPart(input_str)]))
    results = list(method(results))
    return "".join([result.replacement for result in results if isinstance(result, TextPart)])

class ValueResolver:
    """
    Resolves variables, special keys, and escape sequences in the input string.
    """

    def __init__(self, input_string, variables_obj, special_keys):
        """
        Initialize a ValueResolver instance.

        Args:
            input_string (str): The input string to be resolved.
            variables_obj (object): An object containing variables.
            special_keys (object): An object containing special keys.
        """
        self.input_string = input_string
        self.variables = variables_obj
        self.special_keys = special_keys

    @staticmethod
    def resolve(input_string, variables_obj, special_keys):
        """
        Resolve variables, special keys, and escape sequences in the input string.

        Args:
            input_string (str): The input string to be resolved.
            variables_obj (object): An object containing variables.
            special_keys (object): An object containing special keys.

        Returns:
            list: A list of resolved parts as strings.
        """
        if input_string is not None:
            # Create an instance of ValueResolver and initiate the resolution process
            value_resolver = ValueResolver(input_string, variables_obj, special_keys)

            input_ = [TextPart(value_resolver.input_string)]

            # Resolve escape sequences (if any) in the final results
            results = list(value_resolver.resolve_escapes_in_parts(input_))

            # Resolve special keys in the input string
            results = list(value_resolver.resolve_special_keys_in_parts(results))

            # Resolve variables in the results from the previous step
            results = list(value_resolver.resolve_variables_in_parts(results))

            return [result.replacement for result in results if isinstance(result, TextPart)]
        return []

    @staticmethod
    def resolve_special_keys(input_str, special_keys):
        """
        Resolve special keys in the input string.

        Args:
            input_str (str): The input string to be resolved.
            special_keys (object): An object containing special keys.

        Returns:
            str: The resolved input string with special keys replaced.
        """
        value_resolver = ValueResolver(input_str, None, special_keys)
        return _resolve_as_str(value_resolver.resolve_escapes_in_parts, value_resolver.resolve_special_keys_in_parts, input_str)

    @staticmethod
    def resolve_variables(input_str, variables_obj):
        """
        Resolve variables in the input string.

        Args:
            input_str (str): The input string to be resolved.
            variables_obj (object): An object containing variables.

        Returns:
            str: The resolved input string with variables replaced.
        """
        value_resolver = ValueResolver(input_str, variables_obj, None)
        return _resolve_as_str(value_resolver.resolve_escapes_in_parts, value_resolver.resolve_variables_in_parts, input_str)


    def resolve_special_keys_in_parts(self, input_parts):
        """
        Resolve special keys in the input parts.

        Args:
            input_parts (list): List of TextPart instances representing parts of the input string.

        Yields:
            TextPart or SpecialKeyPart: Yields the resolved TextPart or SpecialKeyPart instance.
        """
        for input_part in input_parts:
            if type(input_part) is TextPart:
                # Split the input string for each keyword coated in []
                parts = re.split(r"(?<!\\)\[([\w]+)(?<!\\)\]", input_part.text)

                for part in parts:
                    # Check if the input_part is a special key present in the special_keys object
                    if part in vars(self.special_keys):
                        # If the input_part is a special key, yield its corresponding value
                        yield SpecialKeyPart(part, getattr(self.special_keys, part))
                    elif part != "":
                        # If the input_part is not a special key, yield it as it is
                        yield TextPart(part)
            else:
                yield input_part

    def resolve_variables_in_parts(self, input_parts):
        """
        Resolve variables in the input parts.

        Args:
            input_parts (list): List of TextPart instances representing parts of the input string.

        Yields:
            TextPart or VariablePart: Yields the resolved TextPart or VariablePart instance.
        """
        for input_part in input_parts:
            if type(input_part) is TextPart:
                # Split the input_part and find variables represented with $ sign
                parts = re.split(r'(?<!\\)\$([\w]+(?:\.[\w]+)*)', input_part.text)

                for part in parts:
                    variable_value = self.variables
                    variable_parts = part.split('.')

                    # Check if the first part of the variable exists in the variables_obj
                    if len(variable_parts) > 0 and variable_parts[0] in vars(variable_value):
                        # If the variable is found, resolve the chain of variable names to get its value
                        for variable_part in variable_parts:
                            variable_value = getattr(variable_value, variable_part)

                        # Yield the final resolved value of the variable
                        yield VariablePart(part, variable_value)
                    elif part != "":
                        # If the variable is not found, yield it as it is
                        yield TextPart(part)
            else:
                yield input_part

    def resolve_escapes_in_parts(self, input_parts):
        """
        Resolve escape sequences in the input parts.

        Args:
            input_parts (list): List of TextPart instances representing parts of the input string.

        Yields:
            TextPart or EscapedPart: Yields the resolved TextPart or EscapedPart instance.
        """
        for input_part in input_parts:
            if type(input_part) is TextPart:
                parts = re.split(r"(\\\\|\\[$[\]])", input_part.text)

                for part in parts:
                    if any([part.startswith(f"\\{char}") for char in ("\\", "$", "[", "]")]):
                        # If the part contains a backslash, yield it as an EscapedPart
                        yield EscapedPart(part, part[-1])
                    else:
                        # If there is no backslash, yield it as a TextPart
                        yield TextPart(part)
            else:
                yield input_part

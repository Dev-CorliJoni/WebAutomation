from WebInterface.helper.special_char import SpecialChar
from selenium.webdriver.common.keys import Keys

class StringReplacer:

    @staticmethod
    def resolve_variables(value: str, data) -> str:
        """
        Resolves variables in the given value by replacing them with their corresponding values from the data object.

        :param value: The string value possibly containing variables.
        :param data: The data object that contains the variable values.
        
        :return: The value with variables replaced by their values.
        """

        return_value = ""

        for variable_name in StringReplacer.get_elements_by_markers(value, SpecialChar.DOLLAR, SpecialChar.END_MARKERS, False):
            # Check if the data object has the variable
            if hasattr(data, variable_name):
                variable_content = getattr(data, variable_name)

                # If the variable content is a list, join its elements into a string
                if type(variable_content) is list:
                    variable_content = ", ".join(variable_content)
            else:
                raise Exception(f"[VariableNotAvailable]: Variable ${variable_name} is not available")

            # Replace the variable with its corresponding value in the return value
            # value[:value.find(variable_name) - 1] -> The -1 removes $
            return_value = f"{return_value}{value[:value.find(variable_name) - 1]}{variable_content}"
            value = value[value.find(variable_name) + len(variable_name):]

        return f"{return_value}{value}"

    @staticmethod
    def resolve_special_keys(value: str):
        """
        Resolves special keys in the given value by replacing them with their corresponding values from the Keys class.

        :param value: The string value possibly containing special keys.
        
        :yields: The resolved special keys or the remaining value.
        """

        elements = StringReplacer.get_elements_by_markers(value, SpecialChar.OPEN_SQUARE_BRACKET, [SpecialChar.CLOSING_SQUARE_BRACKET])

        for key_name in elements:
            # Check if the Keys class has the special key
            if hasattr(Keys, key_name):
                key_content = getattr(Keys, key_name)
            else:
                raise Exception(f"[KeyNotAvailable]: Key [{key_name}] is not available")

            # Yield the value till the key occurs and the key_content
            # value[:value.find(key_name) - 1] -> The -1 removes [
            yield value[:value.find(key_name) - 1]
            yield key_content

            # value[value.find(key_name) + len(key_name) + 1:] -> The +1 removes ]
            value = value[value.find(key_name) + len(key_name) + 1:]

        if value != "":
            yield value

    @staticmethod
    def get_elements_by_markers(value: str, start_marker: str, end_markers: list[str], is_end_marker_necessary=True):
        """
        Retrieves elements from the value that are enclosed by start and end markers.

        :param value: The string value to search for elements.
        :param start_marker: The start marker for identifying elements.
        :param end_markers: The list of possible end markers for identifying elements.
        :param is_end_marker_necessary: Flag indicating if an end marker is required.
        
        :yields: The elements found between the markers.
        """

        start_index = value.find(start_marker)
        end_index = StringReplacer._get_end_index(value, end_markers, start_index)

        while start_marker in value and (StringReplacer._are_end_markers_in_value(value, end_markers, start_index) or not is_end_marker_necessary):
            yield value[start_index + 1:end_index]

            if len(value) > end_index and value[end_index] == SpecialChar.CLOSING_SQUARE_BRACKET:
                end_index = end_index + 1

            value = value[end_index:len(value)]

            start_index = value.find(start_marker)
            end_index = StringReplacer._get_end_index(value, end_markers, start_index)

    @staticmethod
    def _get_end_index(value: str, end_markers: list[str], start_index: int) -> int:
        """
        Retrieves the index of the first occurrence of an end marker in the value.

        :param value: The string value to search for end markers.
        :param end_markers: The list of possible end markers.
        :param start_index: The index to start searching from.
        
        :returns: The index of the first occurrence of an end marker, or the length of the value if no end marker is found.
        """

        end_marker_indexes = [value.find(end_marker, start_index + 1) for end_marker in end_markers if end_marker in value[start_index+1:]]
        return min(end_marker_indexes, default=len(value))

    @staticmethod
    def _are_end_markers_in_value(value: str, end_markers: list[str], start_index: int) -> bool:
        """
        Checks if any of the end markers are present in the value after the start index.

        :param value: The string value to check for end markers.
        :param end_markers: The list of possible end markers.
        :param start_index: The index to start checking from.

        :returns: True if any end marker is found, False otherwise.
        """

        return any([end_marker in value[start_index:] for end_marker in end_markers])

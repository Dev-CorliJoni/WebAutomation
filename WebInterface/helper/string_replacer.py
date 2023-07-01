from WebInterface.helper.special_char import SpecialChar
from selenium.webdriver.common.keys import Keys

class StringReplacer:

    @staticmethod
    def resolve_variables(value, data):

        return_value = ""

        for variable_name in StringReplacer.get_elements_by_markers(value, SpecialChar.DOLLAR, SpecialChar.END_MARKERS, False):

            if hasattr(data, variable_name):
                variable_content = getattr(data, variable_name)

                if type(variable_content) is list:
                    variable_content = ", ".join(variable_content)
            else:
                raise Exception(f"[VariableNotAvailable]: Variable ${variable_name} is not available")

            # value[:value.find(variable_name) - 1] -> The -1 removes $
            return_value = f"{return_value}{value[:value.find(variable_name) - 1]}{variable_content}"
            value = value[value.find(variable_name) + len(variable_name):]

        return f"{return_value}{value}"

    @staticmethod
    def resolve_special_keys(value):
        elements = StringReplacer.get_elements_by_markers(value, SpecialChar.OPEN_SQUARE_BRACKET, [SpecialChar.CLOSING_SQUARE_BRACKET])

        for variable_name in elements:

            if hasattr(Keys, variable_name):
                variable_content = getattr(Keys, variable_name)
            else:
                raise Exception(f"[KeyNotAvailable]: Key [{variable_name}] is not available")

            # value[:value.find(variable_name) - 1] -> The -1 removes $
            yield value[:value.find(variable_name) - 1]
            yield variable_content

            value = value[value.find(variable_name) + len(variable_name) + 1:]

        if value != "":
            yield value

    @staticmethod
    def get_elements_by_markers(value: str, start_marker: str, end_markers: str, is_end_marker_necessary=True):
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
    def _get_end_index(value, end_markers, start_index):
        end_marker_indexes = [value.find(end_marker, start_index + 1) for end_marker in end_markers if end_marker in value[start_index+1:]]
        return min(end_marker_indexes, default=len(value))

    @staticmethod
    def _are_end_markers_in_value(value, end_markers, start_index):
        return any([end_marker in value[start_index:] for end_marker in end_markers])


from WebInterface.element_interaction_web_interface import ElementInteractionWebInterface


def _create_control_collection_by_list(web_interface, control_references, controls):
    """
    Create a collection of controls based on a list of control references.

    :param web_interface: The web interface object.
    :param control_references: The list of control references.
    :param controls: The Session.Controls object.
    :yield: Yields the resolved controls.
    """
    for control_reference in control_references:
        if hasattr(controls, control_reference):
            yield getattr(controls, control_reference)
        else:
            yield ElementInteractionWebInterface.resolve(web_interface, control_reference)


def _create_control_collection_by_str(web_interface, xpath_controls: str):
    """
    Create a collection of controls based on an XPath string.

    :param web_interface: The web interface object.
    :param xpath_controls: The XPath string.
    :return: The resolved controls as a list.
    """
    return ElementInteractionWebInterface.resolve_many(web_interface, xpath_controls)


class ControlCollections:
    """
    This class contains all mappings between a name and a list of controls.
    """

    def __init__(self, web_interface, control_collections, controls):
        """
        Initializes the ControlCollections object.

        :param web_interface: The web interface object.
        :param control_collections: A dictionary mapping name and either a list of control_references or an XPath string.
        :param controls: The Session.Controls object that holds every HTML element of interest.
        """
        for name, control_references in control_collections:
            if isinstance(control_references, str):
                setattr(self, name, list(_create_control_collection_by_str(web_interface, control_references)))
            else:  # List
                setattr(self, name, list(_create_control_collection_by_list(web_interface, control_references, controls)))

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        """
        Iterates over the ControlCollections object.

        :yield: Yields the name and value of each attribute.
        """
        for name in vars(self):
            yield name, getattr(self, name)

from WebInterface.element_interaction_web_interface import ElementInteractionWebInterface


class Controls:
    """
    Class that contains all mapped HTML elements.
    """

    def __init__(self, web_interface: "WebInterface", control_configuration):
        """
        Initializes the Controls object.

        For each name and XPath mapping, an attribute is declared in this class,
        which holds the resolved element of the XPath.

        :param web_interface: The web interface object.
        :param control_configuration: A mapping of names to XPath strings.
        """
        for name, xpath in control_configuration:
            setattr(self, name, ElementInteractionWebInterface.resolve(web_interface, xpath))

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        """
        Iterates over the Controls object.

        :yield: Yields the name and value of each attribute.
        """
        for name in vars(self):
            yield name, getattr(self, name)

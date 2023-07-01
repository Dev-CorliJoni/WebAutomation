from WebInterface.element_interaction_web_interface import ElementInteractionWebInterface


class Controls:
    """
    Class that contains all mapped HTML elements
    """

    def __init__(self, web_interface, control_configuration):
        """
        For each name, x-path mapping a attribute is declared in this class, which holds the resolved element of the xpath.
        :param control_configuration: A mapping of names to a x-path
        """
        for name, xpath in control_configuration:
            setattr(self, name, ElementInteractionWebInterface.resolve(web_interface, xpath))

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for name in vars(self):
            yield name, getattr(self, name)

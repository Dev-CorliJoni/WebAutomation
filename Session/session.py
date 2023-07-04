from Session import Controls, ControlCollections, DataHandler


class Session:
    """
    The Session class is a partial representation of the requested website.
    It contains representations of the controls defined in the configuration.
    These controls can be collected as control_collections.
    In addition, this class contains the data to which all variables defined in this context belong.
    """

    def __init__(self, web_interface):
        """
        Initializes the Session object.

        :param web_interface: The web interface object.
        """
        self.web_interface = web_interface

        self.data = DataHandler()
        self.controls = None
        self.control_collections = None

        self.update_configuration({}, {})

    def update_configuration(self, control_configuration: dict, control_collections: dict) -> None:
        """
        Updates the configuration of controls and control collections.

        :param control_configuration: A dictionary mapping control names to their XPath.
        :param control_collections: A dictionary mapping control collection names to either a list of control references or an XPath.
        """
        self.controls = Controls(self.web_interface, control_configuration)
        self.control_collections = ControlCollections(self.web_interface, control_collections, self.controls)

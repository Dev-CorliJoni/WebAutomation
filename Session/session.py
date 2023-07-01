from Session import Controls, ControlCollections, DataHandler


class Session:
    """
    The Session class is a partial representation of the requested website.
    It contains representations of the controls defined in the configuration.
    These controls can be collected as control_collections.
    In addition, this class contains the data to which all variables defined in this context belong.
    """

    def __init__(self, web_interface):
        self.web_interface = web_interface

        self.data = DataHandler()
        self.controls = None
        self.control_collections = None

        self.update_configuration({}, {})

    def update_configuration(self, control_configuration, control_collections):
        self.controls = Controls(self.web_interface, control_configuration)
        self.control_collections = ControlCollections(self.web_interface, control_collections, self.controls)

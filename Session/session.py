from Session import Controls, ControlCollections, DataHandler


class Session:
    """
    The Session class is a partial representation of the requested website.
    It contains representations of the controls defined in the configuration.
    These controls can be collected as control_collections.
    In addition, this class contains the data to which all variables defined in this context belong.
    """

    def __init__(self, driver, wait):
        self._driver = driver
        self.wait = wait

        self.data = DataHandler()
        self.controls = None
        self.control_collections = None

        self.update_configuration({}, {})

    def update_configuration(self, control_configuration, control_collections):
        self.controls = Controls(self._driver, self.wait, control_configuration)
        self.control_collections = ControlCollections(self._driver, self.wait, control_collections, self.controls)

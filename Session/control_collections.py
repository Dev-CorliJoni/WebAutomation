from Session import resolve, resolve_many


def _create_control_collection_by_list(driver, wait, control_references, controls):
    for control_reference in control_references:
        if hasattr(controls, control_reference):
            yield getattr(controls, control_reference)
        else:
            yield resolve(driver, wait, control_reference)


def _create_control_collection_by_str(driver, wait, xpath_controls):
    return resolve_many(driver, wait, xpath_controls)


class ControlCollections:
    """
    This class contains all mappings between a name and list of controls
    """

    def __init__(self, driver, wait, control_collections, controls):
        """
        :param control_collections: A dictionary, mapping name and either a list of control_references or a x-path str
        :param controls: A Session.Controls object, that holds every HTML element of interest
        """
        
        for name, control_references in control_collections:
            if type(control_references) is str:
                setattr(self, name, list(_create_control_collection_by_str(driver, wait, control_references)))
            else:  # List
                setattr(self, name, list(_create_control_collection_by_list(driver, wait, control_references, controls)))

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for name in vars(self):
            yield name, getattr(self, name)

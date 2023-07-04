def _has_attributes(obj, *attributes):
    """
    Checks if an object has all the specified attributes.

    :param obj: The object to check for attributes.
    :param attributes: Variable number of attributes to check.
    :return: True if the object has all the specified attributes, False otherwise.
    """
    return all([hasattr(obj, attribute) for attribute in attributes])

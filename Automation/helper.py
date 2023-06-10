def _has_attributes(obj, *attributes):
    return all([hasattr(obj, attribute) for attribute in attributes])

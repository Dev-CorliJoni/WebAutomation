class Configuration:
    """
    Represents a configuration object that holds key-value pairs.
    """

    def __init__(self, **configuration):
        """
        Initializes the Configuration object with the given key-value pairs.

        :param configuration: Key-value pairs to populate the configuration.
        """
        self._resolve_dict(configuration)

    def __repr__(self):
        text = {name: str(getattr(self, name)) for name in vars(self)}
        return f"{text}"

    def __iter__(self):
        """
        Iterates over the key-value pairs in the Configuration object.

        :return: Iterator of key-value pairs.
        """
        for key in vars(self):
            yield key, getattr(self, key)

    def _resolve_dict(self, _dict: dict):
        """
        Resolves the dictionary items and sets them as attributes of the Configuration object.

        :param _dict: Dictionary containing the key-value pairs.
        """
        for name, value in _dict.items():
            setattr(self, name, self._resolve_item(value))

    def _generate_list_representation(self, _list):
        """
        Generates the list representation by resolving each item.

        :param _list: List to generate the representation for.
        :return: Generator yielding the resolved items.
        """
        for item in _list:
            yield self._resolve_item(item)

    def _resolve_item(self, item):
        """
        Resolves an item by checking its type and returning the resolved value.

        :param item: Item to resolve.
        :return: Resolved item.
        """
        if type(item) is list:
            return list(self._generate_list_representation(item))
        elif type(item) is dict:
            return Configuration(**item)
        else:
            return item

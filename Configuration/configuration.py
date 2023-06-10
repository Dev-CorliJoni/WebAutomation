class Configuration:

    def __init__(self, **configuration):
        self._resolve_dict(configuration)

    def __repr__(self):
        text = {name: str(getattr(self, name)) for name in vars(self)}
        return f"{text}"

    def __iter__(self):
        for key in vars(self):
            yield key, getattr(self, key)

    def _resolve_dict(self, _dict: dict):
        for name, value in _dict.items():
            setattr(self, name, self._resolve_item(value))

    def _generate_list_representation(self, _list):
        for item in _list:
            yield self._resolve_item(item)

    def _resolve_item(self, item):
        if type(item) is list:
            return list(self._generate_list_representation(item))
        elif type(item) is dict:
            return Configuration(**item)
        else:
            return item

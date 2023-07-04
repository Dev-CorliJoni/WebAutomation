class DataHandler:
    """
    Class that handles data operations.
    """

    def __init__(self) -> None:
        self._data = Data()

    def __setitem__(self, name: str, value: any) -> None:
        return setattr(self._data, name, value)

    def __getitem__(self, name: str) -> any:
        return getattr(self._data, name)

    def __setattr__(self, name: str, value: any) -> None:
        if name == "_data":
            super(DataHandler, self).__setattr__(name, value)
        else:
            setattr(self._data, name, value)

    def __getattribute__(self, name: str) -> any:
        if name == "_data":
            return super(DataHandler, self).__getattribute__(name)
        else:
            return getattr(self._data, name)

    def __delattr__(self, name: str) -> None:
        if name == "_data":
            return super(DataHandler, self).__delattr__(name)
        else:
            return delattr(self._data, name)

    def __iter__(self):
        for name in vars(self._data):
            yield name, getattr(self._data, name)

    def __str__(self) -> str:
        return str(dict(self))

    def __len__(self) -> int:
        return len(vars(self))


class Data:
    pass

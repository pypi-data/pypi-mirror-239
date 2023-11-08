from .base_type import DataType


class BOOL(DataType):
    _format = '?'
    _base_type = bool

    @property
    def val(self) -> bool:
        return self._val

    @val.setter
    def val(self, value: bool):
        self.validation(value)
        self._val = value

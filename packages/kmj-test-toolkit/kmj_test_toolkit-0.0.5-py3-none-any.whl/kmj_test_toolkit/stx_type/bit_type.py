from .base_type import IntegerBase


class BYTE(IntegerBase):
    _format = 'B'


class WORD(IntegerBase):
    _format = 'H'


class DWORD(IntegerBase):
    _format = 'I'


class LWORD(IntegerBase):
    _format = 'Q'

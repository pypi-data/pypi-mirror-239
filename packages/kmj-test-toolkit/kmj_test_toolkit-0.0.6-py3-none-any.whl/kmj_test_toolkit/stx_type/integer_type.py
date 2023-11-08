from .base_type import IntegerBase


class SINT(IntegerBase):
    _format = 'b'


class INT(IntegerBase):
    _format = 'h'


class DINT(IntegerBase):
    _format = 'i'


class LINT(IntegerBase):
    _format = 'q'


class USINT(IntegerBase):
    _format = 'B'


class UINT(IntegerBase):
    _format = 'H'


class UDINT(IntegerBase):
    _format = 'I'


class ULINT(IntegerBase):
    _format = 'Q'

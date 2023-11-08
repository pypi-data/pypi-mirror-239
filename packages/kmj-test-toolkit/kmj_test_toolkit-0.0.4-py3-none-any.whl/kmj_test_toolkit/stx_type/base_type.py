from __future__ import annotations

from .exception import InvalidBaseTypeException

from typing import Literal

import struct

from abc import ABCMeta, abstractmethod

TYPE_BYTE_ORDER = Literal['@', '=', '<', '>', '!']
BYTE_ORDER: TYPE_BYTE_ORDER = '<'


class STXType(metaclass=ABCMeta):
    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @property
    @abstractmethod
    def format(self) -> str:
        pass

    @property
    @abstractmethod
    def val(self):
        pass

    @val.setter
    @abstractmethod
    def val(self, value):
        pass

    @abstractmethod
    def pack(self) -> bytes:
        pass

    @abstractmethod
    def unpack(self, buffer: bytes, start_idx: int = 0):
        pass


class DataType(STXType, metaclass=ABCMeta):
    _base_type: type
    _format: str

    def __init__(self, init_val: _base_type = None):
        cls = self.__class__
        if init_val is None:
            self._val: cls._base_type = cls._base_type()
        else:
            self.validation(init_val)
            self._val = init_val

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._val})"

    def validation(self, value):
        cls = self.__class__
        if not isinstance(value, cls._base_type):
            raise InvalidBaseTypeException(value, cls._base_type)

    @property
    def size(self) -> int:
        return struct.calcsize(self.format)

    @property
    def format(self) -> str:
        return self._format

    @property
    def base_type(self) -> type:
        return self._base_type

    def pack(self) -> bytes:
        return struct.pack(f'{BYTE_ORDER}{self.format}', self._val)

    def unpack(self, buffer: bytes, start_idx: int = 0):
        start = start_idx
        end = start_idx + self.size
        unpacked: tuple = struct.unpack(f'{BYTE_ORDER}{self.format}', buffer[start:end])
        self.val = unpacked[0]


class IntegerBase(DataType):
    _base_type = int

    def __init__(self, init_val: _base_type = None):
        cls = self.__class__
        if init_val is not None and isinstance(init_val, float):
            if (init_val % 1) == 0:
                init_val = int(init_val)
            else:
                raise InvalidBaseTypeException(init_val, cls._base_type)
        super().__init__(init_val)

    @property
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, value: int):
        if isinstance(value, float):
            try:
                value = int(value)
            except TypeError:
                raise InvalidBaseTypeException
        self.validation(value)
        self._val = value


class FloatBase(DataType):
    _base_type = float

    def __init__(self, init_val: _base_type = None):
        if init_val is not None and isinstance(init_val, int):
            init_val = float(init_val)
        super().__init__(init_val)

    @property
    def val(self) -> float:
        return self._val

    @val.setter
    def val(self, value: float):
        if isinstance(value, int):
            value = float(value)
        self.validation(value)
        self._val = value

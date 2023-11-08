from __future__ import annotations

from .base_type import STXType
from typing import TypeVar


T = TypeVar('T', bound=STXType)


class Array(STXType):
    def __init__(self, base_type: type[T], array_shape: list[int] = None, shape_attr: str = None):
        self._val: list[STXType] = []
        self._array_shape = array_shape
        self._base_type = base_type
        self._format = ''
        self._size = 0
        self.shape_attr = shape_attr
        if array_shape is not None:
            self.__create_array()

    def __repr__(self):
        return f'{self._val}'

    def __getitem__(self, idx: int) -> T | Array:
        return self._val[idx]

    def __class_getitem__(cls, array_base_type: type[T]) -> type[T]:
        return array_base_type

    def __iter__(self):
        return iter(self._val)

    def has_shape(self) -> bool:
        return self._array_shape is not None

    def from_shape(self, shape: list[int] | int):
        if isinstance(shape, int):
            shape = [shape]
        self._array_shape = shape
        self.__create_array()

    def __create_array(self):
        if len(self._array_shape) > 1:
            self.__create_child_array()
        else:
            array_length = self._array_shape[0]
            for _ in range(array_length):
                element: T = self._base_type()
                self._val.append(element)
                self._format += element.format
                self._size += element.size

    def __create_child_array(self):
        array_length: int
        child_shape: list[int]
        array_length, *child_shape = self._array_shape

        for _ in range(array_length):
            element = Array(self._base_type, child_shape)
            self._val.append(element)
            self._format += element.format
            self._size += element.size

    @property
    def size(self) -> int:
        return self._size

    @property
    def format(self) -> str:
        return self._format

    @property
    def val(self) -> list:
        return [element.val for element in self._val]

    @val.setter
    def val(self, value: list):
        array_length = self._array_shape[0]
        for idx in range(array_length):
            self[idx].val = value[idx]

    @property
    def base_type(self) -> type[T]:
        return self._base_type

    def pack(self) -> bytes:
        packed: bytes = b''
        for element in self._val:
            packed += element.pack()
        return packed

    def unpack(self, buffer: bytes, start_idx: int = 0):
        for element in self._val:
            element.unpack(buffer, start_idx)
            start_idx += element.size

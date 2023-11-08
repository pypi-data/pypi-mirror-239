from __future__ import annotations

from .exception import ShapeAttrNotFoundException
from .base_type import STXType, DataType
from .array_type import Array
from typing import Any
from copy import deepcopy


class Structure(STXType):
    def __new__(cls, **kwargs):
        obj = super().__new__(cls)
        element_names: list[str] = []
        for key, member in cls.__annotations__.items():
            member_object = cls.__dict__.get(key)
            if member_object:
                instance = deepcopy(member_object)

                if isinstance(member_object, Array):
                    if not instance.has_shape():
                        shape: list[int] = kwargs.get(member_object.shape_attr)
                        if shape is None:
                            raise ShapeAttrNotFoundException(member_object.shape_attr)
                        instance.from_shape(shape)
                    obj.__dict__[key] = instance

                elif isinstance(member_object, STXType):
                    obj.__dict__[key] = instance
                element_names.append(key)

            else:
                if issubclass(member, STXType):
                    obj.__dict__[key] = member()
                    element_names.append(key)
        obj._element_names = element_names
        return obj

    def __init__(self, *args, **kwargs):
        self._size = 0
        self._format = ''

    def __repr__(self) -> str:
        cls = self.__class__
        inner = ", ".join([f"{key}={element}" for key, element in self.items()])
        return f"{cls.__name__}({inner})"

    def __getitem__(self, key: str) -> STXType:
        items = {name: self.__dict__[name] for name in self._element_names}
        return items[key]

    def keys(self) -> list[str]:
        return self._element_names

    def values(self) -> list[STXType]:
        return [self[key] for key in self.keys()]

    def items(self) -> list[tuple[str, STXType]]:
        return [(key, self[key]) for key in self.keys()]

    @property
    def size(self) -> int:
        if self._size == 0:
            self._size = sum([element.size for element in self.values()])
        return self._size

    @property
    def format(self) -> str:
        if self._format == '':
            self._format = ''.join([element.format for element in self.values()])
        return self._format

    @property
    def val(self) -> dict[str, Any]:
        return {key: element.val for key, element in self.items()}

    @val.setter
    def val(self, dict_obj: dict[str, any]):
        for key, v in self.items():
            if isinstance(v, DataType):
                temp = v.base_type(dict_obj[key])
                v.val = temp
            else:
                v.val = dict_obj[key]

    def update(self, dict_obj: dict[str, any]):
        for key, v in self.items():
            obj_val = dict_obj.get(key)
            if obj_val is None:
                continue
            if isinstance(v, DataType):
                temp = v.base_type(dict_obj[key])
                v.val = temp
            else:
                v.val = dict_obj[key]

    def pack(self) -> bytes:
        packed = b''
        for element in self.values():
            packed += element.pack()
        return packed

    def unpack(self, buffer: bytes, start_idx: int = 0):
        for element in self.values():
            element.unpack(buffer, start_idx)
            start_idx += element.size

from __future__ import annotations

from .base_type import STXType, BYTE_ORDER

import struct


class STRING(STXType):
    _base_type: type[str] = str

    def __init__(self, init_size: int, init_val: str = ''):
        self._format = f"{init_size}s"
        self._size = struct.calcsize(f"{init_size}s")
        self._val = init_val

    def __repr__(self) -> str:
        return f"STRING[{self._size}]('{self._val}')"

    @property
    def size(self) -> int:
        return self._size

    @property
    def format(self) -> str:
        return f"{self._size}s"

    @property
    def val(self) -> str:
        return self._val

    @val.setter
    def val(self, value: str | bytes):
        if isinstance(value, bytes):
            value = value.decode("utf-8").replace("\0", "")
        self._val = value

    def pack(self) -> bytes:
        return struct.pack(f"{BYTE_ORDER}{self.format}", self._val.encode("utf-8"))

    def unpack(self, buffer: bytes, start_idx: int = 0):
        start = start_idx
        end = start_idx + self.size
        unpacked: tuple = struct.unpack(f"{BYTE_ORDER}{self.format}", buffer[start:end])
        self.val = unpacked[0]

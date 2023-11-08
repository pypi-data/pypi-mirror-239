class InvalidBaseTypeException(Exception):
    def __init__(self, init_val, base_type: type):
        self.init_val = init_val
        self.base_type = base_type

    def __str__(self) -> str:
        return f"initial value '{self.init_val}' is not valid base type '{self.base_type}'"


class ShapeAttrNotFoundException(Exception):
    def __init__(self, shape_attr: str):
        self.shape_attr = shape_attr

    def __str__(self) -> str:
        return f"attr '{self.shape_attr}' must be required"

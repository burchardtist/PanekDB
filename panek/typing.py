from typing import Type, TypeVar

__all__ = [
    'Object',
    'ObjectType',
    'Object1',
    'Object2',
]


Object = TypeVar('Object')
ObjectType = Type[Object]

Object1 = TypeVar('Object1')
Object2 = TypeVar('Object2')

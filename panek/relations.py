from abc import ABC
from dataclasses import dataclass, field

from uuid import UUID, uuid4

__all__ = [
    'Relation',
    'ManyRelation',
    'OneRelation',
]


@dataclass(frozen=True)
class Relation(ABC):
    to_type: type
    id: UUID = field(default_factory=uuid4, init=False)


@dataclass(frozen=True)
class ManyRelation(Relation):
    to_type: type


@dataclass(frozen=True)
class OneRelation(Relation):
    """
    substitution - able to set if relation doesn't exist or is None but cannot
    replace object with another object.

    If substitution is False only way to set another relation is remove old
    and then add new.
    """
    to_type: type
    substitution: bool = False

__all__ = [
    'ObjectRelationError',
    'SubstitutionNotAllowedError',
    'ManySameRelationsError',
    'MissingRelationError',
    'InvalidRelationError',
]


class ObjectRelationError(Exception):
    pass


class SubstitutionNotAllowedError(ObjectRelationError):
    pass


class ManySameRelationsError(ObjectRelationError):
    pass


class MissingRelationError(ObjectRelationError):
    pass


class InvalidRelationError(ObjectRelationError):
    pass

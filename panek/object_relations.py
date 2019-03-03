from abc import ABC
from dataclasses import dataclass
from typing import Dict, Optional, Set
from uuid import UUID

import panek.typing as t
from panek.error import InvalidRelationError, ManySameRelationsError, \
    MissingRelationError, SubstitutionNotAllowedError
from panek.relations import ManyRelation, OneRelation, Relation
from panek.utils import method_dispatch

__all__ = [
    'ObjectRelationMapper'
]


@dataclass(frozen=True)
class RelationFields:
    rel1: Relation
    rel2: Relation


class RelationOperationsDispatcher(ABC):
    """
    Takes care of relation operations: get, add, remove.
    Every operation has method dispatch for OneRelation and ManyRelation.
    """

    def __init__(self):
        self._container: Dict[UUID, Set[t.Object]] = dict()

    # GET #####################################################################
    @method_dispatch
    def get_relation(self, relation: Relation):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
        )

    @get_relation.register
    def _get_many(self, relation: ManyRelation) -> Optional[Set[t.Object]]:
        return self._container.get(relation.id)

    @get_relation.register
    def _get_one(self, relation: OneRelation) -> Optional[t.Object]:
        obj = self._container.get(relation.id)
        return list(obj)[0] if obj else None

    # ADD #####################################################################
    @method_dispatch
    def _add_relation(self, relation: Relation, related: t.Object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
        )

    @_add_relation.register
    def _many_add(self, relation: ManyRelation, related: t.Object):
        container = self._container
        id_ = relation.id

        if id_ not in container.keys():
            container[id_] = set()
        container[id_].add(related)

    @_add_relation.register
    def _one_add(self, relation: OneRelation, related: t.Object):
        self._container[relation.id] = {related}

    # REMOVE ##################################################################
    @method_dispatch
    def _remove_relation(self, relation: Relation, related: t.Object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
        )

    @_remove_relation.register
    def _many_remove(self, relation: ManyRelation, related: t.Object):
        container = self._container
        id_ = relation.id
        try:
            container[id_].remove(related)
        except KeyError:
            raise MissingRelationError

    @_remove_relation.register
    def _one_remove(self, relation: OneRelation, related: t.Object):
        container = self._container
        id_ = relation.id

        try:
            del container[id_]
        except KeyError:
            raise MissingRelationError


class ObjectsContainer(ABC):
    """
    Holds objects of the same type.
    Keeps self._add_objects and self._remove_objects as protected methods.
    """

    def __init__(self):
        self._objects: Dict[t.ObjectType, Set[t.Object]] = dict()

    def get_type(self, type_: t.ObjectType) -> Set[t.Object]:
        return self._objects.get(type_) or set()

    def _add_objects(self, *objects: t.Object):
        objects_dict = self._objects
        for obj in objects:
            type_id = type(obj)
            if type_id not in objects_dict.keys():
                objects_dict[type_id] = set()
            objects_dict[type_id].add(obj)

    def _remove_objects(self, *objects: t.Object):
        objects_dict = self._objects
        for obj in objects:
            objects_dict[type(obj)].remove(obj)


class ObjectRelationMapper(RelationOperationsDispatcher, ObjectsContainer):
    """
    Entry class to keep all objects bounded in relations.
    Ensures that objects are kept equally on the both sides of relations
    """
    def __init__(self):
        RelationOperationsDispatcher.__init__(self)
        ObjectsContainer.__init__(self)
        self._relations: Dict[int, Relation] = dict()

    def _seek_relations(self, obj: t.Object) -> Relation:
        return self._relations.get(obj) or self._setup_relation(obj)

    def _setup_relation(self, obj: t.Object) -> Relation:
        relations = {
            getattr(obj, x) for x in dir(obj)
            if isinstance(getattr(obj, x), Relation)
        }

        if not len(relations) == 1:
            raise ManySameRelationsError

        relation = relations.pop()
        self._relations[obj] = relation

        return relation

    def _get_relations(self, obj1: t.Object1, obj2: t.Object2) -> RelationFields:
        return RelationFields(
            rel1=self._seek_relations(obj1),
            rel2=self._seek_relations(obj2),
        )

    def _one_to_one_substitution(self, relations: RelationFields):
        rel1: OneRelation = relations.rel1
        rel2: OneRelation = relations.rel2
        rel1_object = self.get_relation(rel1)
        rel2_object = self.get_relation(rel2)

        if rel1_object or rel2_object:
            if not rel1.substitution or not rel2.substitution:
                raise SubstitutionNotAllowedError
            if rel1_object:
                relation = self._relations[rel1_object]
                self._remove_relation(relation, None)
            if rel2_object:
                relation = self._relations[rel2_object]
                self._remove_relation(relation, None)

    def _one_to_many_substitution(self, one_relation, to_remove):
        if self.get_relation(one_relation):
            if not one_relation.substitution:
                raise SubstitutionNotAllowedError
            relation = self._relations[self.get_relation(one_relation)]
            self._remove_relation(relation, to_remove)

    def _ensure_substitution(
        self,
        obj1: t.Object1,
        obj2: t.Object2,
        relations: RelationFields
    ):
        """
        Provides substitution for one-to-many and one-to-one relations.

        If substitution is allowed and ManyRelation contains already
        the object to substitute remove it from this relation
        to ensure that it will not be duplicated.
        """
        if (isinstance(relations.rel1, OneRelation) and
                isinstance(relations.rel2, OneRelation)):
            return self._one_to_one_substitution(relations)

        elif isinstance(relations.rel1, OneRelation):
            one_relation = relations.rel1
            to_remove = obj1

        elif isinstance(relations.rel2, OneRelation):
            one_relation = relations.rel2
            to_remove = obj2

        # many-to-many: do nothing.
        else:
            return

        self._one_to_many_substitution(one_relation, to_remove)

    def add(self, obj1: t.Object1, obj2: t.Object2):
        relations = self._get_relations(obj1, obj2)
        self._ensure_substitution(obj1, obj2, relations)
        self._add_relation(relations.rel1, obj2)
        self._add_relation(relations.rel2, obj1)
        self._add_objects(obj1, obj2)

    def remove(self, obj1: t.Object1, obj2: t.Object2):
        relations = self._get_relations(obj1, obj2)
        self._remove_relation(relations.rel1, obj2)
        self._remove_relation(relations.rel2, obj1)

        if not self.get_relation(relations.rel1):
            self._remove_objects(obj1)
        if not self.get_relation(relations.rel2):
            self._remove_objects(obj2)

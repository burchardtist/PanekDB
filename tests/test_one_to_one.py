import pytest

from panek.error import SubstitutionNotAllowedError
from tests.conftest import Ssn, SsnPerson, SsnPersonSubstitution, \
    SsnSubstitution, TestPersonSsn, TestPersonSsnSubstitute


def test_add_one(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm

    assert orm.get_relation(person.ssn) is ssn
    assert orm.get_relation(ssn.person) is person
    assert len(orm.get_type(SsnPerson)) == 1
    assert len(orm.get_type(Ssn)) == 1


def test_remove_one(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm
    orm.remove(person, ssn)

    assert orm.get_relation(person.ssn) is None
    assert orm.get_relation(ssn.person) is None
    assert not orm.get_type(SsnPerson)
    assert not orm.get_type(Ssn)


def test_substitution_not_allowed(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm
    another_ssn = Ssn()
    another_person = SsnPerson()

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(person, another_ssn)

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(another_person, ssn)

    assert orm.get_relation(person.ssn) is ssn
    assert orm.get_relation(ssn.person) is person


def test_substitution_not_allowed_with_one_substitution(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm
    ssn_substitution = SsnSubstitution()
    person_substitution = SsnPersonSubstitution()

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(person, ssn_substitution)

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(person_substitution, ssn)

    assert orm.get_relation(person.ssn) is ssn
    assert orm.get_relation(ssn.person) is person


def test_substitution_allowed_ssn(substitution_orm: TestPersonSsnSubstitute):
    orm, person, ssn = substitution_orm
    another_ssn = SsnSubstitution()

    orm.add(person, ssn)
    orm.add(person, another_ssn)

    assert orm.get_relation(person.ssn) is another_ssn
    assert orm.get_relation(ssn.person) is None
    assert orm.get_relation(another_ssn.person) is person


def test_substitution_allowed_person(substitution_orm: TestPersonSsnSubstitute):
    orm, person, ssn = substitution_orm
    another_person = SsnPersonSubstitution()

    orm.add(person, ssn)
    orm.add(another_person, ssn)

    assert orm.get_relation(ssn.person) is another_person
    assert orm.get_relation(person.ssn) is None
    assert orm.get_relation(another_person.ssn) is ssn


def test_substitution_allowed_person_reversed(substitution_orm: TestPersonSsnSubstitute):
    orm, person, ssn = substitution_orm
    another_person = SsnPersonSubstitution()

    orm.add(person, ssn)
    orm.add(ssn, another_person)

    assert orm.get_relation(ssn.person) is another_person
    assert orm.get_relation(person.ssn) is None
    assert orm.get_relation(another_person.ssn) is ssn

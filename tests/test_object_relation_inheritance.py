from tests.conftest import Cabin, Cottage, House, SAMPLE_SIZE, TestObjects


def test_add_many_types(many_orm: TestObjects):
    orm, person, houses = many_orm
    total_size = SAMPLE_SIZE * len([House, Cabin])

    assert len(houses) == total_size
    assert not [x for x in houses if isinstance(x, Cottage)]

    cottage = Cottage()
    orm.add(person, cottage)
    person_houses = orm.get_relation(person.houses)

    assert len(person_houses) == total_size + 1
    assert len([x for x in person_houses if isinstance(x, Cottage)]) == 1


def test_get_many_types(many_orm: TestObjects):
    orm, person, houses = many_orm

    person_houses = orm.get_relation(person.houses)
    cabins = [x for x in person_houses if isinstance(x, Cabin)]
    houses = [x for x in person_houses if isinstance(x, House)]

    assert all([orm.get_relation(house.person) is person for house in houses])
    assert len(cabins) == SAMPLE_SIZE
    assert len(houses) == SAMPLE_SIZE
    assert len(person_houses) == len(cabins) + len(houses)


def test_remove_many_types(many_orm: TestObjects):
    orm, person, houses = many_orm

    cabins = [x for x in houses if isinstance(x, Cabin)]

    for cabin in cabins:
        orm.remove(person, cabin)

    person_houses = orm.get_relation(person.houses)
    assert not [x for x in person_houses if isinstance(x, Cabin)]
    assert len([x for x in person_houses if isinstance(x, House)]) == SAMPLE_SIZE
    assert len(person_houses) == SAMPLE_SIZE

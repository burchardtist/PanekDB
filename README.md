# PanekDB
![python](https://img.shields.io/badge/python-3.7.1-informational.svg) ![Coverage](/tests/coverage.svg)

Object Relation Mapper for python objects kept in the memory. 
Use this tool to wrap with more compact system. Check examples in tests 
but also take a look at my other project 
[Entity Component System](https://github.com/burchardtist/byt)
where is a complete usage of _PanekDB_.

### Usage
To run the tool just run:
```python
orm = ObjectRelationMapper()
``` 

Let's implement example models:
```python
class House:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person)

class Person:
    def __init__(self):
        self.houses: ManyRelation = ManyRelation(to_type=IHouse)
```

#### **IMPORTANT**
Setup relations inside `__init__` method to make sure that relation will have unique id.
 
 
Available `ObjectRelationMapper` methods:

```python
# Setup some model objects
house = House()
person = Person()
```

- `add` 

Add both objects as related.
```python
orm.add(house, person)
```

- `remove`

Remove this relation.
```python
orm.remove(house, person)
```

- `get_relation`

Get all objects of the relation.
It's important to provide to the method desired relation instead of object.
```python
orm.get_relation(person.houses)
```

- `get_type`

Get all objects of desired type that actually have any relation.
Notice that class type is provided as attribute.
```python
orm.get_type(Person)
```

### Relation types
`ObjectRelationMapper` handles:
- one-to-many
- one-to-one
- many-to-many

#### OneRelation
This relation contains one extra option such as `substitution`.

By default `substitution` is set as `False` which means that if relation actually
has any active relation it will be raised `SubstitutionNotAllowedError`

```python
house = House()
another_house = House()
person = Person()

orm.add(house, person)
orm.add(another_house, person)  # Error!
```

But still you can remove and then add new relation:
```python
orm.remove(house, person)
orm.add(another_house, person)  # Now it's fine
```

##### Allow substitution
To allow substitution set `substitution=True` in constructor:
```python
class SubstitutionHouse:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person, substitution=True)
```

Now it is possible to replace relation in the fly:
```python
house = SubstitutionHouse()
another_house = SubstitutionHouse()
person = Person()

orm.add(house, person)
orm.add(another_house, person)  # Success!

house_substitution = SubstitutionHouse()
orm.remove(house, person)
orm.add(another_house, person)  # It also works
```

---
### To do list
- [ ] Add possibility to make `ObjectRelationMapper` as a global object to 
let `Relation` directly perform actions. 

- [ ] Change `get_relation` to pass object directly instead of its relation. 

- [ ] Add multiple relations.
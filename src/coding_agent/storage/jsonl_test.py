# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest
from pydantic import BaseModel

from coding_agent.storage.jsonl import JsonlDatabase


class Person(BaseModel):
    name: str
    age: int


@pytest.fixture
def tmp_db_file(tmp_path: Path) -> Path:
    return tmp_path / "test_database.jsonl"


@pytest.fixture
def db(tmp_db_file: Path) -> JsonlDatabase[Person]:
    return JsonlDatabase(Person, tmp_db_file)


def test_init_and_load(tmp_db_file: Path):
    # Create a database with some initial data
    initial_data = [Person(name="Alice", age=30), Person(name="Bob", age=25)]
    db = JsonlDatabase(Person, tmp_db_file)
    for person in initial_data:
        db.append(person)

    # Create a new instance to test loading
    db2 = JsonlDatabase(Person, tmp_db_file)
    assert len(db2.get_all()) == 2
    assert db2[0].name == "Alice"
    assert db2[1].age == 25


def test_append_and_get_all(db: JsonlDatabase[Person]):
    db.append(Person(name="Charlie", age=35))
    db.append(Person(name="David", age=40))

    assert len(db.get_all()) == 2
    assert db[0].name == "Charlie"
    assert db[1].age == 40


def test_get_latest(db: JsonlDatabase[Person]):
    db.append(Person(name="Eve", age=28))
    db.append(Person(name="Frank", age=45))

    latest = db.get_latest()
    assert latest is not None
    assert latest.name == "Frank"
    assert latest.age == 45


def test_get_latest_empty_db(tmp_db_file: Path):
    empty_db = JsonlDatabase(Person, tmp_db_file)
    assert empty_db.get_latest() is None


def test_wrong_model(tmp_db_file: Path):
    db = JsonlDatabase(Person, tmp_db_file)
    db.append(Person(name="Grace", age=32))

    class WrongPerson(BaseModel):
        name: str
        height: float

    with pytest.raises(ValueError):
        JsonlDatabase(WrongPerson, tmp_db_file)


def test_persistence(tmp_db_file: Path):
    db1 = JsonlDatabase(Person, tmp_db_file)
    db1.append(Person(name="Hannah", age=50))

    db2 = JsonlDatabase(Person, tmp_db_file)
    assert len(db2.get_all()) == 1
    latest = db2.get_latest()
    assert latest is not None
    assert latest.name == "Hannah"

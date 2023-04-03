import pytest as pytest

from sdp.fast_db import FastDB, FastDBIndex, FastDBStorage
from tests.fast_db.model import User


@pytest.mark.parametrize("db_class", [FastDB])
def test_db(tmp_path, db_class):
    db = db_class(tmp_path)

    pmerienne = User(first_name='Pierre', last_name='Merienne')
    juchanut = User(first_name='Julie', last_name='Chanut')
    gboole = User(first_name='George', last_name='Boole')

    db.set('pmerienne', pmerienne)
    db.set('juchanut', juchanut)
    db.set('gboole', gboole)

    assert db.get('pmerienne') == pmerienne
    assert db.get('juchanut') == juchanut
    assert db.get('gboole') == gboole
    assert db.get('unknown') is None

    db.close()

    db = db_class(tmp_path)
    assert db.get('pmerienne') == pmerienne
    assert db.get('juchanut') == juchanut
    assert db.get('gboole') == gboole
    assert db.get('unknown') is None


@pytest.mark.parametrize("index_class", [FastDBIndex])
def test_index(tmp_path, index_class):
    index_filepath = tmp_path / "index.db"
    index = index_class(index_filepath)

    assert index.get_position('unknown') is None

    index.set_position('foo', 42)
    index.set_position('foobar', 43)
    index.set_position('foobar', 44)

    assert index.get_position('foo') == 42
    assert index.get_position('foobar') == 44

    index.close()

    index = index_class(index_filepath)
    assert index.get_position('foo') == 42
    assert index.get_position('foobar') == 44


@pytest.mark.parametrize("storage_class", [FastDBStorage])
def test_storage(tmp_path, storage_class):
    filepath = tmp_path / "data.db"
    storage = storage_class(filepath)

    position_foo = storage.write_value({'foo': 'bar'})
    position_123 = storage.write_value(123)

    assert storage.read_value(position_foo) == {'foo': 'bar'}
    assert storage.read_value(position_123) == 123

    storage.close()
    storage = storage_class(filepath)

    assert storage.read_value(position_foo) == {'foo': 'bar'}
    assert storage.read_value(position_123) == 123


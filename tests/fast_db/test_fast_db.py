from sdp.fast_db import FastDB, FastDBIndex
from tests.fast_db.model import User


def test_everything(tmp_path):
    db = FastDB(tmp_path)

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

    db = FastDB(tmp_path)
    assert db.get('pmerienne') == pmerienne
    assert db.get('juchanut') == juchanut
    assert db.get('gboole') == gboole
    assert db.get('unknown') is None


def test_index(tmp_path):
    index_filepath = tmp_path / "index.db"
    index = FastDBIndex(index_filepath)

    assert index.get_position('unknown') is None

    index.set_position('foo', 42)
    index.set_position('foobar', 43)
    index.set_position('foobar', 44)

    assert index.get_position('foo') == 42
    assert index.get_position('foobar') == 44

    index.close()

    index = FastDBIndex(index_filepath)
    assert index.get_position('foo') == 42
    assert index.get_position('foobar') == 44



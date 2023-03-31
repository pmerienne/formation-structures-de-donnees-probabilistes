import pytest

from sdp.hash_table.dict import ListBasedDict, PythonDict, ChainedHashTable


@pytest.mark.parametrize("dict_class", [PythonDict, ListBasedDict, ChainedHashTable])
def test_get_and_set(dict_class):
    my_dict = dict_class()
    my_dict.set('hello', 'Pierre')
    my_dict.set(42, 'foo')
    my_dict.set(42, 'foobar')

    assert my_dict.get('hello') == 'Pierre'
    assert my_dict.get(42) == 'foobar'
    assert my_dict.get('42') is None

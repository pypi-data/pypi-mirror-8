from mock import patch
import pytest

from nameko.exceptions import (
    serialize, deserialize, deserialize_to_instance, RemoteError,
    UnserializableValueError)


class CustomError(Exception):
    pass


@pytest.yield_fixture
def registry():
    with patch('nameko.exceptions.registry', {}) as patched:
        yield patched


def test_serialize():

    exc = CustomError('something went wrong')

    assert serialize(exc) == {
        'exc_type': 'CustomError',
        'exc_path': 'test.test_exceptions.CustomError',
        'exc_args': ('something went wrong',),
        'value': 'something went wrong',
    }


def test_serialize_cannot_unicode():

    class CannotUnicode(object):
        def __str__(self):
            raise Exception('boom')

    bad_string = CannotUnicode()
    exc = CustomError(bad_string)

    assert serialize(exc) == {
        'exc_type': 'CustomError',
        'exc_path': 'test.test_exceptions.CustomError',
        'exc_args': (bad_string,),
        'value': '[__unicode__ failed]',
    }


def test_deserialize_to_remote_error():

    exc = CustomError('something went wrong')
    data = serialize(exc)

    deserialized = deserialize(data)
    assert type(deserialized) == RemoteError
    assert deserialized.exc_type == "CustomError"
    assert deserialized.value == "something went wrong"
    assert str(deserialized) == "CustomError something went wrong"


@pytest.mark.usefixtures('registry')
def test_deserialize_to_instance():

    # register Error as deserializable to an instance
    deserialize_to_instance(CustomError)

    exc = CustomError('something went wrong')
    data = serialize(exc)

    deserialized = deserialize(data)
    assert type(deserialized) == CustomError
    assert str(deserialized) == "something went wrong"


def test_exception_name_clash():

    class MethodNotFound(Exception):
        # application exception with clashing name
        pass

    exc = MethodNotFound('application error')
    data = serialize(exc)

    deserialized = deserialize(data)
    assert type(deserialized) == RemoteError
    assert deserialized.exc_type == "MethodNotFound"
    assert deserialized.value == "application error"
    assert str(deserialized) == "MethodNotFound application error"

    from nameko.exceptions import MethodNotFound as NamekoMethodNotFound

    exc = NamekoMethodNotFound('missing')
    data = serialize(exc)

    deserialized = deserialize(data)
    assert type(deserialized) == NamekoMethodNotFound
    assert str(deserialized) == "missing"


def test_serialize_backwards_compat():

    exc = CustomError('something went wrong')
    data = serialize(exc)

    # nameko < 1.5.0 has no ``exc_path`` or ``exc_args`` keys
    del data['exc_path']
    del data['exc_args']

    deserialized = deserialize(data)
    assert type(deserialized) == RemoteError
    assert deserialized.exc_type == "CustomError"
    assert deserialized.value == "something went wrong"
    assert str(deserialized) == "CustomError something went wrong"

    # nameko < 1.1.4 has an extra ``traceback`` key
    data['traceback'] = "traceback string"

    deserialized = deserialize(data)
    assert type(deserialized) == RemoteError
    assert deserialized.exc_type == "CustomError"
    assert deserialized.value == "something went wrong"
    assert str(deserialized) == "CustomError something went wrong"


def test_unserializable_value_error():

    # normal value
    value = "value"
    exc = UnserializableValueError(value)

    assert exc.repr_value == "'value'"
    assert str(exc) == "Unserializable value: `'value'`"

    # un-repr-able value
    class CannotRepr(object):
        def __repr__(self):
            raise Exception('boom')

    bad_value = CannotRepr()
    exc = UnserializableValueError(bad_value)

    assert exc.repr_value == "[__repr__ failed]"
    assert str(exc) == "Unserializable value: `[__repr__ failed]`"

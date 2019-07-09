from kanpai import Kanpai
import pytest


def test_error_when_data_is_not_array():
    schema = Kanpai.Array()
    result = schema.validate('not an array')
    assert result.get('success') is False


def test_error_if_data_is_none_when_required():
    schema = Kanpai.Array().required()
    result = schema.validate(None)
    assert result.get('success') is False


def test_sucees_if_data_is_proper_when_required():
    schema = Kanpai.Array().required()
    result = schema.validate([12, 45])
    assert result.get('success') is True


def test_error_when_element_validation_error():
    schema = Kanpai.Array().of(Kanpai.Object({
        'name': Kanpai.String().trim().required(),
        'age': Kanpai.Number().integer()
    })).required()

    result = schema.validate([
        {
            'name': '  Rpose ion  ',
            'age': 46
        },
        {
            'age': '98'
        }
    ])

    assert result.get('success') is False
    assert result.get('error').get(1, None) is not None


def test_success_when_element_validation_success():
    schema = Kanpai.Array().of(Kanpai.Object({
        'name': Kanpai.String().trim().required(),
        'age': Kanpai.Number().integer()
    })).required()

    result = schema.validate([
        {
            'name': '  Rpose ion  ',
            'age': 46
        },
        {
            'age': '98',
            'name': 'Mert rt'
        }
    ])

    assert result.get('success') is True


def test_error_when_invalid_element_validator():
    with pytest.raises(TypeError):
        Kanpai.Array().of("kanpai").required()


def test_success_when_element_validation_on_none_data():
    schema = Kanpai.Array().of(Kanpai.Object({
        'name': Kanpai.String().trim().required(),
        'age': Kanpai.Number().integer()
    }))

    result = schema.validate(None)

    assert result.get('success') is True


def test_error_when_minimum_element_not_there():
    schema = Kanpai.Array().of(Kanpai.String()).min(1)
    result = schema.validate([])
    assert result.get('success') is False


def test_error_when_more_than_maximum_element():
    schema = Kanpai.Array().of(Kanpai.String()).max(3)
    result = schema.validate(['CKP', 'RZSD', 'LOMP', 'LKUIO'])
    assert result.get('success') is False

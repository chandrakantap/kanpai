from kanpai import Kanpai
import pytest


def test_validate_string():
    schema = Kanpai.String(error="Text expected")
    result = schema.validate('kanpai')
    assert result['success'] is True
    assert result['error'] is None


def test_error_on_validate_string():
    schema = Kanpai.String(error="Text expected")
    result = schema.validate({'name': 'kanpai'})
    assert result['success'] is False
    assert result['error'] is not None


def test_handle():
    schema = Kanpai.String(error="Field must be a text.").max(
        5, error="Maximum allowed value is 5").min(2, error="Minimum required value is 2")
    result = schema.validate('asdasdasdasdas dasd a sdadsad')
    assert result['success'] is False
    assert result['error'] is not None
    assert result['error'] == "Maximum allowed value is 5"


def test_success_when_data_is_none_if_not_required():
    schema = Kanpai.String().trim().max(34)
    result = schema.validate(None)
    assert result.get('success') is True


def test_error_when_data_is_none_if_required():
    schema = Kanpai.String().trim().max(34).required()
    result = schema.validate(None)
    assert result.get('success') is False


def test_error_when_data_is_empty_if_required():
    schema = Kanpai.String().trim().max(34).required()
    result = schema.validate('         ')
    assert result.get('success') is False


def test_success_when_string_length_is_below_max():
    schema = Kanpai.String().trim().max(12)
    result = schema.validate('kanpai')
    assert result.get('success') is True


def test_error_when_string_length_is_above_max():
    schema = Kanpai.String().trim().max(10).required()
    result = schema.validate('kanpai string length above 10')
    assert result.get('success') is False


def test_error_when_max_length_data_type_is_not_int():
    with pytest.raises(ValueError):
        Kanpai.String().trim().max(10.00)


def test_success_when_string_length_is_above_min():
    schema = Kanpai.String().trim().min(12)
    result = schema.validate('kanpai string length above 12 char')
    assert result.get('success') is True


def test_error_when_string_length_is_below_min():
    schema = Kanpai.String().trim().min(10).required()
    result = schema.validate('kanpai')
    assert result.get('success') is False


def test_error_when_min_length_data_type_is_not_int():
    with pytest.raises(ValueError):
        Kanpai.String().trim().min(10.00)


def test_fail_when_value_not_from_choice():
    '''anyof test'''
    schema = Kanpai.String().trim().anyof(('PY', 'JAVA', 'TS'))
    result = schema.validate('kanpai')
    assert result.get('success') is False


def test_sucess_when_data_is_none_for_anyof():
    '''anyof test'''
    schema = Kanpai.String().trim().anyof(('PY', 'JAVA', 'TS'))
    result = schema.validate(None)
    assert result.get('success') is True


def test_sucess_when_data_is_in_choice_anyof():
    '''anyof test'''
    schema = Kanpai.String().trim().anyOf(('PY', 'JAVA', 'TS'))
    result = schema.validate('TS')
    assert result.get('success') is True


def test_should_not_mutate():
    validator = Kanpai.String().trim().required()
    full_name = "   Quentin Tarantino "
    sresult = validator.validate(full_name)
    assert sresult == {
        'success': True,
        'error': None,
        'data': 'Quentin Tarantino'
    }

    assert full_name == "   Quentin Tarantino "

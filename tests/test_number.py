from kanpai import Kanpai
import pytest


def test_error_if_data_is_not_number_or_equivalent():
    schema = Kanpai.Number()
    result = schema.validate({'a': 10})
    assert result.get('success') is False


def test_error_if_data_is_not_covertable_to_number():
    schema = Kanpai.Number()
    result = schema.validate('1234kanpai')
    assert result.get('success') is False


def test_success_if_data_is_integer():
    schema = Kanpai.Number()
    result = schema.validate(345)
    assert result.get('success') is True
    assert result.get('data') is not None
    assert type(result.get('data')) is float


def test_success_if_data_is_float():
    schema = Kanpai.Number()
    result = schema.validate(345.89)
    assert result.get('success') is True
    assert result.get('data') is not None
    assert type(result.get('data')) is float


def test_success_if_data_is_string_formatted_integer():
    schema = Kanpai.Number()
    result = schema.validate('345')
    assert result.get('success') is True
    assert result.get('data') is not None
    assert type(result.get('data')) is float


def test_success_if_data_is_string_formatted_float():
    schema = Kanpai.Number()
    result = schema.validate('345.89')
    assert result.get('success') is True
    assert result.get('data') is not None
    assert type(result.get('data')) is float


def test_success_convert_data_to_integer():
    schema = Kanpai.Number().integer()
    result = schema.validate('345.89')
    assert result.get('success') is True
    assert result.get('data') is not None
    assert result.get('data') == 345
    assert type(result.get('data')) is int


def test_error_if_data_is_none_when_required():
    schema = Kanpai.Number().integer().required('This value is required.')
    result = schema.validate(None)
    assert result.get('success') is False
    assert result.get('error') is not None
    assert result.get('error') == 'This value is required.'


def test_success_when_data_is_none_and_not_required():
    schema = Kanpai.Number().integer().min(12).max(34).between(12, 34)
    result = schema.validate(None)
    assert result.get('success') is True
    assert result.get('data') is None
    assert result.get('error') is None


def test_success_when_data_is_not_none_and_required():
    schema = Kanpai.Number().integer().required().min(12).max(34).between(12, 34)
    result = schema.validate(30)
    assert result.get('success') is True
    assert result.get('data') == 30
    assert result.get('error') is None


def test_error_on_invalid_start_range_data_type():
    with pytest.raises(ValueError):
        Kanpai.Number().required().between('qwe', 34)


def test_error_on_invalid_end_range_data_type():
    with pytest.raises(ValueError):
        Kanpai.Number().required().between(65, 'adasd')


def test_error_when_data_is_under_the_range():
    schema = Kanpai.Number().between(12.45, 45.89, 'Data must be within range.')
    result = schema.validate('10.59')
    assert result.get('success') is False
    assert result.get('data') == '10.59'
    assert result.get('error') == 'Data must be within range.'


def test_error_when_data_is_over_the_range():
    schema = Kanpai.Number().between(12.45, 45.89, 'Data must be within range.')
    result = schema.validate('45.90')
    assert result.get('success') is False
    assert result.get('data') == '45.90'
    assert result.get('error') == 'Data must be within range.'


def test_error_when_data_is_start_of_the_range():
    schema = Kanpai.Number().between(12.45, 45.89, 'Data must be within range.')
    result = schema.validate('12.45')
    assert result.get('success') is True
    assert result.get('data') == 12.45
    assert result.get('error') is None


def test_error_when_data_is_end_of_the_range():
    schema = Kanpai.Number().between(12.45, 45.89, 'Data must be within range.')
    result = schema.validate(45.89)
    assert result.get('success') is True
    assert result.get('data') == 45.89
    assert result.get('error') is None


def test_error_when_data_is_between_the_range():
    schema = Kanpai.Number().between(12.45, 45.89, 'Data must be within range.')
    result = schema.validate(40)
    assert result.get('success') is True
    assert result.get('data') == 40.00
    assert result.get('error') is None


def test_error_on_invalid_max_data_type():
    with pytest.raises(ValueError):
        Kanpai.Number().required().max('qwe')


def test_error_on_invalid_min_data_type():
    with pytest.raises(ValueError):
        Kanpai.Number().required().min('qwe')


def test_error_when_data_is_higer_than_max():
    schema = Kanpai.Number().max(12.45, error='Data must be less than or equal 12.45.')
    result = schema.validate(40)
    assert result.get('success') is False
    assert result.get('data') == 40.00
    assert result.get('error') == 'Data must be less than or equal 12.45.'


def test_success_when_data_is_max_value():
    schema = Kanpai.Number().max(12.45, error='Data must be less than or equal 12.45.')
    result = schema.validate(12.45)
    assert result.get('success') is True
    assert result.get('data') == 12.45
    assert result.get('error') is None


def test_success_when_data_is_less_than_max_value():
    schema = Kanpai.Number().integer().max(12.45, error='Data must be less than or equal 12.45.')
    result = schema.validate(9)
    assert result.get('success') is True
    assert result.get('data') == 9
    assert result.get('error') is None


def test_error_when_data_is_less_than_min():
    schema = Kanpai.Number().min(12.45, error='Minimum value must 12.45.')
    result = schema.validate(6)
    assert result.get('success') is False
    assert result.get('data') == 6.00
    assert result.get('error') == 'Minimum value must 12.45.'


def test_success_when_data_is_min_value():
    schema = Kanpai.Number().min(12.45, error='Minimum value must 12.45.')
    result = schema.validate(12.45)
    assert result.get('success') is True
    assert result.get('data') == 12.45
    assert result.get('error') is None


def test_success_when_data_is_higher_than_min_value():
    schema = Kanpai.Number().integer().min(12.45, error='Data must be less than or equal 12.45.')
    result = schema.validate(90)
    assert result.get('success') is True
    assert result.get('data') == 90
    assert result.get('error') is None

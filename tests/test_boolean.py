from kanpai import Kanpai


def test_error_if_data_is_none_when_required():
    schema = Kanpai.Boolean().required('This value is required.')
    result = schema.validate(None)
    assert result.get('success') is False
    assert result.get('error') is not None
    assert result.get('error') == 'This value is required.'


def test_success_when_data_is_none_and_not_required():
    schema = Kanpai.Boolean()
    result = schema.validate(None)
    assert result.get('success') is True
    assert result.get('data') is None
    assert result.get('error') is None


def test_error_if_data_is_not_boolean_or_equivalent():
    schema = Kanpai.Boolean()
    result = schema.validate({'a': 10})
    assert result.get('success') is False


def test_error_if_data_is_not_boolean():
    schema = Kanpai.Boolean()
    result = schema.validate(123)
    assert result.get('success') is False


def test_error_if_extended_but_invalid_value():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate('123')
    assert result.get('success') is False


def test_success_if_data_is_boolean():
    schema = Kanpai.Boolean()
    result = schema.validate(True)
    assert result.get('success') is True
    assert result.get('data') is not None
    assert type(result.get('data')) is bool


def test_success_extended_yes():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate('Yes')
    assert result.get('success') is True
    assert result.get('data') is True
    assert type(result.get('data')) is bool


def test_success_extended_no():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate('No')
    assert result.get('success') is True
    assert result.get('data') is False
    assert type(result.get('data')) is bool


def test_success_extended_true():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate('True')
    assert result.get('success') is True
    assert result.get('data') is True
    assert type(result.get('data')) is bool


def test_success_extended_false():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate('False')
    assert result.get('success') is True
    assert result.get('data') is False
    assert type(result.get('data')) is bool


def test_success_extended_number():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate(1234)
    assert result.get('success') is True
    assert result.get('data') is True
    assert type(result.get('data')) is bool


def test_success_extended_number_0():
    schema = Kanpai.Boolean(extended=True)
    result = schema.validate(0)
    assert result.get('success') is True
    assert result.get('data') is False
    assert type(result.get('data')) is bool

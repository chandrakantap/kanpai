from kanpai import Kanpai


def test_error_if_not_valid_uuid():
    schema = Kanpai.UUID(error="UUID expected")
    result = schema.validate('')
    assert result['success'] is False
    assert result['error'] == 'UUID expected'


def test_error_if_object_passed():
    schema = Kanpai.UUID(error="UUID expected")
    result = schema.validate({'name': 'Kanpai'})
    assert result['success'] is False
    assert result['error'] == 'UUID expected'


def test_error_blank_on_required():
    schema = Kanpai.UUID(error="UUID expected").required()
    result = schema.validate(None)
    assert result['success'] is False
    assert result['error'] == 'Value is required'


def test_success_for_valid_uuid():
    schema = Kanpai.UUID(error="UUID expected")
    result = schema.validate('393505c9-e789-4f20-a7b7-1e7104ec728e')
    assert result['success'] is True
    assert result['error'] is None

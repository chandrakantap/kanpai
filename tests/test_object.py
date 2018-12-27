import kanpai as Kanpai
import pytest


def test_error_if_schema_is_not_dict():
    with pytest.raises(ValueError, match=r'Expecting schema to be a dictionary'):
        Kanpai.Object('kanpai')


def test_error_if_schema_member_is_not_validator():
    with pytest.raises(TypeError):
        Kanpai.Object({
            'name': Kanpai.String().required(),
            'age': 31
        })


def test_should_validate_properly():
    schema = Kanpai.Object({
        'name': Kanpai.String('User name must be string').trim().required('Please provide user name'),
        'company': Kanpai.String('Company must be string').trim().required('Please provide company name')
    })

    result = schema.validate({
        'name': '    Chandrakanta     ',
        'company': 'kanpai     '
    })

    assert result.get('success') is True
    assert result.get('data') is not None
    assert result.get('data').get('name') == 'Chandrakanta'
    assert result.get('data').get('company') == 'kanpai'


def test_error_on_extra_key_if_ignore_false():
    schema = Kanpai.Object({
        'name': Kanpai.String('User name must be string').trim().required('Please provide user name'),
        'company': Kanpai.String('Company must be string').trim().required('Please provide company name')
    }, ignore_extra_key=False)

    result = schema.validate({
        'name': '    Chandrakanta     ',
        'company': 'kanpai     ',
        'age': 32
    })

    assert result.get('success') is False
    assert result.get('error') is not None
    assert result.get('error').get('age') is not None

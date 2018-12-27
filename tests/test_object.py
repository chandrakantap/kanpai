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


def test_success_if_value_is_none_when_not_required():
    schema = Kanpai.Object({
        'name': Kanpai.String()
    })

    result = schema.validate(None)

    assert result.get('success') is True


def test_error_if_value_is_none_when_required():
    schema = Kanpai.Object({
        'name': Kanpai.String()
    }).required()

    result = schema.validate(None)

    assert result.get('success') is False


def test_error_when_required_inner_object_none():
    SCHEMA = Kanpai.Object({
        'phone': Kanpai.Object({
            'country_code': Kanpai.String().trim().required().max(3),
            'phone_number': Kanpai.String().trim().required().max(10)
        }).required("Please provide phone number.")
    })

    result = SCHEMA.validate({

    })

    assert result.get('success') is False
    assert result.get('error').get('phone') is not None
    assert result.get('error').get('phone') == 'Please provide phone number.'


def test_success_when_optional_inner_object_none():
    SCHEMA = Kanpai.Object({
        'name': Kanpai.String().required(),
        'phone': Kanpai.Object({
            'country_code': Kanpai.String().trim().required().max(3),
            'phone_number': Kanpai.String().trim().required().max(10)
        })
    })

    result = SCHEMA.validate({
        'name': 'Kanpai'
    })

    assert result.get('success') is True
    assert result.get('error') is  None

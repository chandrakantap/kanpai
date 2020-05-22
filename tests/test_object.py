from kanpai import Kanpai
import pytest
from uuid import UUID


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
        'name': (Kanpai.String('User name must be string')
                 .trim()
                 .required('Please provide user name')),
        'company': (Kanpai.String('Company must be string')
                    .trim()
                    .required('Please provide company name'))
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
        'name': (Kanpai.String('User name must be string')
                 .trim()
                 .required('Please provide user name')),
        'company': (Kanpai.String('Company must be string')
                    .trim()
                    .required('Please provide company name'))
    }, ignore_extra_key=False)

    result = schema.validate({
        'name': '    Chandrakanta     ',
        'company': 'kanpai     ',
        'age': 32
    })

    assert result.get('success') is False
    assert result.get('error') is not None
    assert result.get('error').get('age') is not None


def test_success_on_extra_key_if_ignore_true():
    schema = Kanpai.Object({
        'name': (Kanpai.String('User name must be string')
                 .trim()
                 .required('Please provide user name')),
        'company': (Kanpai.String('Company must be string')
                    .trim()
                    .required('Please provide company name'))
    }, ignore_extra_key=True)

    result = schema.validate({
        'name': '    Chandrakanta     ',
        'company': 'kanpai     ',
        'age': 32
    })

    assert result.get('success') is True
    assert result.get('error') is None
    assert result.get('data').get('age') == 32


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


def test_success_if_value_is_present_when_required():
    schema = Kanpai.Object({
        'name': Kanpai.String()
    }).required()

    result = schema.validate({'name': 'kanpai'})

    assert result.get('success') is True


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
    assert result.get('error') is None


def test_error_when_data_is_not_dict_type():
    schema = Kanpai.Object({
        'name': Kanpai.String()
    })
    result = schema.validate(['its not a dict'])
    assert result.get('success') is False
    assert result.get('error').get('data') is not None


def test_default_error_when_fields_not_equal():
    schema = Kanpai.Object({
        'name': Kanpai.String().required(),
        'password': Kanpai.String().trim().required(),
        'confirm_password': Kanpai.String().trim().required()
    }).assert_equal_field('password', 'confirm_password')

    result = schema.validate({
        'name': 'Kanpai',
        'password': 'Magic@moments',
        'confirm_password': 'separate_one'
    })

    assert result.get('success') is False
    assert result.get('error') == {
        'confirm_password': 'password and confirm_password must be same.'
    }


def test_user_defined_error_when_fields_not_equal():
    schema = Kanpai.Object({
        'name': Kanpai.String().required(),
        'password': Kanpai.String().trim().required(),
        'confirm_password': Kanpai.String().trim().required()
    }).assert_equal_field('password', 'confirm_password',
                          error="Please re-type password correctly.")

    result = schema.validate({
        'name': 'Kanpai',
        'password': 'Magic@moments',
        'confirm_password': 'separate_one'
    })

    assert result.get('success') is False
    assert result.get('error') == {
        'confirm_password': 'Please re-type password correctly.'
    }


def test_success_when_fields_are_equal():
    schema = Kanpai.Object({
        'name': Kanpai.String().required(),
        'password': Kanpai.String().trim().required(),
        'confirm_password': Kanpai.String().trim().required()
    }).assert_equal_field('password', 'confirm_password')

    result = schema.validate({
        'name': 'Kanpai',
        'password': 'Magic@moments',
        'confirm_password': 'Magic@moments'
    })

    assert result.get('success') is True
    assert result.get('error') is None


def test_no_exception_with_equal_validator_when_data_is_none():
    schema = Kanpai.Object({
        'name': Kanpai.String().required(),
        'password': Kanpai.String().trim().required(),
        'confirm_password': Kanpai.String().trim().required()
    }).assert_equal_field('password', 'confirm_password')

    result = schema.validate(None)

    assert result.get('success') is True
    assert result.get('error') is None


def test_successful_validation():
    schema = Kanpai.Object({
        'name': Kanpai.String(),
        'permissions': Kanpai.Array().of(Kanpai.UUID()).required()
    }).required()

    result = schema.validate({
        'permissions': ['a7e459b9-0ec9-41f6-8c78-149ad76c943d']
    })
    assert result == {
        'success': True,
        'data': {
            'permissions': [UUID('a7e459b9-0ec9-41f6-8c78-149ad76c943d')],
            'name': None
        },
        'error': None}


def test_must_validate_all_invalid_data():
    schema = Kanpai.Object({
        'name': Kanpai.String().required(),
        'password': Kanpai.String().trim().required(),
        'confirm_password': Kanpai.String().trim().required()
    }).assert_equal_field('password', 'confirm_password')

    result = schema.validate({})

    assert result.get('success') is False
    assert result.get('error') == {
        'name': 'Value is required',
        'password': 'Value is required',
        'confirm_password': 'Value is required'
    }

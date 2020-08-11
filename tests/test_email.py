import kanpai.email as email

# test non string data


def test_validate_string():
    schema = email.Email()
    result = schema.validate({'name': 'kanpai'})
    assert result['success'] is False
    assert result['error'] is not None


# test 'None' string data
def test_validate_string_on_None_data():
    schema = email.Email()
    result = schema.validate(None)
    assert result['success'] is True
    assert result['error'] is None


# test string data and valid email pattern
def test_validate_stringandpattern_success():
    schema = email.Email()
    result = schema.validate('a@b.com')
    assert result['success'] is True
    assert result['error'] is None


# test string data and invalid email pattern
def test_validate_stringandpattern_failure():
    schema = email.Email(error="Please provide a valid email")
    result = schema.validate('a@bcom')
    assert result['success'] is False
    assert result['error'] is not None
    assert result['error'] == "Please provide a valid email"


# test email as required with data provided
def test_validate_email_required_success():
    schema = (email.Email().trim().required('Email is required'))
    result = schema.validate(' a@b.com')
    assert result['success'] is True
    assert result['error'] is None


# test email as required with blank data provided
def test_error_email_required_blank():
    schema = (email.Email().trim().required('Email is required'))
    result = schema.validate(' ')
    assert result['success'] is False
    assert result['error'] is not None


# test email as required with 'None' data provided
def test_error_email_required_None():
    schema = (email.Email().trim().required('Email is required'))
    result = schema.validate(None)
    assert result['success'] is False
    assert result['error'] is not None

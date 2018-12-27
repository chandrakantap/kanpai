import kanpai as Kanpai


def test_validate_string():
    schema = Kanpai.String(error="Text expected")
    result = schema.validate('kanpai')
    assert result['success'] is True
    assert result['error'] is  None


def test_error_on_validate_string():
    schema = Kanpai.String(error="Text expected")
    result = schema.validate({'name': 'kanpai'})
    assert result['success'] is False
    assert result['error'] is not None

def test_handle():
  schema = Kanpai.String(error="Field must be a text.").max(5,error="Maximum allowed value is 5")
  result = schema.validate('asdasdasdasdas dasd a sdadsad')
  print(result)
  assert result['success'] is False
  assert result['error'] is not None
  assert result['error'] is "Maximum allowed value is 5"

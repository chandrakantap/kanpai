# String Validator

A validator to validate String data.

**Kanpai.String(error="Value must be a string")** - Constructs a String validator. *error* - The error message to return when the data provided for validation is not a String, default - *Value must be a string*

```python
validator = Kanpai.String(error='Please provide an string value.')

#Test with invalid data
result1 = validator.validate(23)
assert result1 == {
  'success':False,
  'error':'Please provide an string value.',
  'data': 23
}

# Test with valid data
result2 = validator.validate('Kanpai')
assert result2 == {
  'success':True,
  'error':None,
  'data': 'Kanpai'
}
```

**Kanpai.String().required(error="Value is required")** - Constructs a String validator and apply required rule. This rule check if the value is present or not. Empty String considered as invalid data.

 *error* - The error message to return when the data provided for validation is not a String, default - *Value is required*

```python
name_validator = Kanpai.String().required(error="Please provide your full name.")

#Test with invalid data
result1 = name_validator.validate(None)
assert result1 == {
  'success':False,
  'error':'Please provide your full name.',
  'data': None
}

result2 = name_validator.validate("")
assert result1 == {
  'success':False,
  'error':'Please provide your full name.',
  'data': ""
}

# Test with valid data
result3 = validator.validate('Kanpai')
assert result3 == {
  'success':True,
  'error':None,
  'data': 'Kanpai'
}
```
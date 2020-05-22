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
## .required()
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
## .trim()
**Kanpai.String().trim()** - Constructs a String validator and apply trim rule. Its not a validation rule its just trim whitespaces from data.Note, trim does not changes original data provided for validation instead works on a copy of that.

trim executes in order its applied.

```python
validator = Kanpai.String().required().trim()

result = validator.validate("  ")
assert result == {
  'success':True,
  'error':None,
  'data': "  "
}
```
:point_up_2: Here trim applied after required, so when required validator applied it was getting data as "  " and validation passed.


```python
validator = Kanpai.String().trim().required()

result = validator.validate("  ")
assert result == {
  'success':False,
  'error':'Value is required',
  'data': "  "
}

# with valid data
full_name = "   Quentin Tarantino "
sresult =  validator.validate(full_name)
assert sresult == {
  'success':True,
  'error':None,
  'data': 'Quentin Tarantino'
}

assert full_name == "   Quentin Tarantino "
```
:point_up_2: Here trim applied before required, so when required validator applied it was getting trimed data and perform validation on that. After successful validation the validaion result contains trimmed data as well, which can be used to store e.g. in db.

Also note, trim does not mutate the original data passed.

## .max() and .min()
**Kanpai.String().max(20,error="Maximum length allowed is 20").min(10,error="Minimum length required is 10")** - Constructs a String validator and apply max and min rule. This rules validate the length of the value.

```python
validator = Kanpai.String().max(20).min(10)
```

- If no value provided, the validation will pass, as these validators do not check for existence of value. Apply *required* validator for that.

```python
assert validator.validate(None) == {
  'success':True,
  'error':None,
  'data': None
}
```

- If empty string provided, the validation will fail, as minimum required is 10

```python
assert validator.validate("") == {
  'success':False,
  'error':"Minimum length required is 10",
  'data': ""
}
```

- If a string with 10 spaces provided , the validation will pass, as minimum required criteria meets.

```python
assert validator.validate("          ") == {
  'success':True,
  'error':None,
  'data': "          "
}
```

- If we use trim before min and provide a string with 10 spaces for validation, the validation will fail as data will be trimmed before *min* validation

```python
another_validator = Kanpai.String().trim().min(10)
assert another_validator.validate("          ") == {
  'success':False,
  'error':"Minimum length required is 10",
  'data': "          "
}
```
:point_up_2: *data* in validation result contains original data as the validation is failed.

## .match()
**Kanpai.String().match(r'[^@]+@[^@]+\.[^@]+',error="pattern doesn't match")** - Constructs a String validator and apply *match* rule. This rule check if the value matched the pattern. Internally the validator use *re.match*. trim will have same effect as of max and min.

```python
import re

re.match(attribs['pattern'], data)
```

```python
validator = Kanpai.String().match(r'[^@]+@[^@]+\.[^@]+')
```

- If no value provided, the validation will pass. use required if you want a value to be present.
```python
assert validator.validate(None) == {
  'success':True,
  'error':None,
  'data': None
}
```

## .anyof()
**Kanpai.String().anyOf(('PY', 'JAVA', 'TS'),error="Invalid data received")** - Constructs a String validator and apply *anyof* rule. This rule check if the data is from list of acceptable values.trim will have same effect as of max and min


```python
validator = Kanpai.String().anyOf(('PY', 'JAVA', 'TS'))
```

- If no value provided, the validation will pass. use required if you want a value to be present.

```python
assert validator.validate(None) == {
  'success':True,
  'error':None,
  'data': None
}
```

```python
#Test with invalid data
result1 = validator.validate("rifol")
assert result1 == {
  'success':False,
  'error':'Invalid data received',
  'data': "rifol"
}

# Test with valid data
result3 = validator.validate('PY')
assert result3 == {
  'success':True,
  'error':None,
  'data': 'PY'
}
```


**kanpai** is a library for validating Python data structures, mainly those coverted from JSON. e.g. JSON received from api request, obtained from config file etc.

Example
-------
Here is a quick example

```python
import kanpai as Kanpai

schema = Kanpai.Object({
        'first_name': (Kanpai.String(error='User first name must be string.')
                       .trim()
                       .required(error='Please provide user first name.')
                       .max(256, error='Maximum allowed length is 256')),

        'last_name': (Kanpai.String(error='User last name must be a String')
                      .trim()
                      .required(error='Please provide user last name.')),
        
        'age'      : (Kanpai.Number(error='Age must be a number.')
                      .max(35,'Maximum allowed age is 35')
                      .min(18,'Age must be minimum 18'))

    })

validation_result = schema.validate({
  'first_name':'Chandrakanta',
  'age': 15
})

assert validation_result == {
  'success': False,
  'error': {
    'last_name': 'Please provide user last name.',
    'age': 'Age must be minimum 18'
  },
  'data': {
     'first_name':'Chandrakanta',
     'age': 15
  }
}
```

```schema.validate``` return a dictionary obejct containing 

```python
{
 'success':'Whether validation is success or not',
 'error':'Validation error',
 'data':'Incase of error data provided for validation , in case success validated data'
}
```


Installation
------------

Use [pip](http://pip-installer.org)

    pip install kanpai


Test
----

```python
pytest # to run tests
pytest --cov-report=html  --cov-branch --cov=kanpai # to generate coverage report
```

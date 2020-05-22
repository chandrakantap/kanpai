**kanpai** is a library for validating Python data structures, mainly those converted from JSON. e.g. JSON received from api request, obtained from config file etc.
The library is built with a focus on better error message. e.g. when validating a dict(which may be converted from JSON), in case of error, Kanpai returns a dict with error details against each keys

# Example

Here is a quick example

```python
from kanpai import Kanpai

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


# Installation


Use [pip](http://pip-installer.org)

    pip install kanpai


# Validators
Validators are the building blocks for Kanpai library. There are validators for different types of data. e.g. String, Array, Object etc. All validators are accessible from Kanpai namespace.

```python
from kanpai import Kanpai

Kanpai.String()
Kanpai.Array()
Kanpai.Boolean()
```
Validation rules can be applied on a validator instance by calling rule methods. All rule method returns `self`. So method calls can be chained. During validaton the rules are checked in order they are applied during validator construction.

Every validator returns an instance of Validator class which has a method called `validate`. Validate takes data to be validated as input and return a dictionary obejct containing:

```python
{
 'success':'Boolean - Whether validation is success or not',
 'error': 'validation error',
 'data':'Incase of error data provided for validation, in case success validated data
}
```
After creating a validator it can be configured to apply validation rule by calling its rule methods. 
After constructing a validator it can be used for multiple validation safely.

For more details on individual validators and its rule methods please refer corresponding file in *docs* folder. 

- **[String Validator](docs/stringvalidator.md#String-Validator)**
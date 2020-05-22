from .validator import Validator
import re


class String(Validator):

    def __assert_required(self, data, attribs):
        if data is None or len(data) == 0:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def required(self, error='Value is required'):
        self.processors.append({
            'action': self.__assert_required,
            'attribs': {
                'error': error
            }
        })
        return self

    def __assert_string(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        data_type = type(data)
        if data_type is int or data_type is float or data_type is str:
            return self.validation_success(str(data))
        else:
            return self.validation_error(data, attribs['error'])

    def __init__(self, error='Value must be a string'):
        self.processors = []
        self.processors.append({
            'action': self.__assert_string,
            'attribs': {
                'error': error
            }
        })

    def __assert_max(self, data, attribs):
        if data is not None and len(data) > attribs['max_length']:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def max(self, max_length, error=None):
        if type(max_length) is not int:
            raise ValueError(
                'value for max_length is expected to be an integer')

        if error is None:
            error = f"Maximum length allowed is {max_length}"

        self.processors.append({
            'action': self.__assert_max,
            'attribs': {
                'max_length': max_length,
                'error': error
            }
        })

        return self

    def __assert_min(self, data, attribs):
        if data is not None and len(data) < attribs['min_length']:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def min(self, min_length, error=None):
        if type(min_length) is not int:
            raise ValueError(
                'value for min_length is expected to be an integer')

        if error is None:
            error = f"Minimum length required is {min_length}"

        self.processors.append({
            'action': self.__assert_min,
            'attribs': {
                'min_length': min_length,
                'error': error
            }
        })

        return self

    def __trim(self, data, attribs):
        if data is None:
            return self.validation_success(None)

        trimmed_data = data.strip()
        if len(data) <= 0:
            return self.validation_success(None)
        else:
            return self.validation_success(trimmed_data)

    def trim(self):
        self.processors.append({
            'action': self.__trim,
            'attribs': None
        })
        return self

    def __assert_pattern(self, data, attribs):
        if data is None:
            return self.validation_success(data)
        if re.match(attribs['pattern'], data):
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs['error'])

    def match(self, pattern, error="pattern doesn't match"):
        self.processors.append({
            'action': self.__assert_pattern,
            'attribs': {
                'error': error,
                'pattern': pattern
            }
        })
        return self

    def __assert_any_of(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        choices = attribs.get('choices', [])
        if data in choices:
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs['error'])

    def anyOf(self, choices=None, error=None):
        return self.anyof(choices, error)

    def anyof(self, choices=[], error="Invalid data received"):
        self.processors.append({
            'action': self.__assert_any_of,
            'attribs': {
                'choices': choices,
                'error': error
            }
        })
        return self

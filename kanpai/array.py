from .validator import Validator, RequiredMixin


class Array(RequiredMixin, Validator):
    def __init__(self, error="Expecting an array.", convert_none_to_empty=False):
        self.processors = []
        self.processors.append({
            'action': self.__assert_array,
            'attribs': {
                'error': error,
                'convert_none_to_empty': convert_none_to_empty
            }
        })

    def __assert_array(self, data, attribs):
        if data is None:
            if attribs.get('convert_none_to_empty', False):
                return self.validation_success([])
            else:
                return self.validation_success(data)

        if type(data) is list or type(data) is tuple:
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs.get('error'))

    def of(self, element_validator):
        if not isinstance(element_validator, Validator):
            raise TypeError(
                f'Expecting a instance of validator in element_validator')

        self.processors.append({
            'action': self.__validate_elements,
            'attribs': {
                'element_validator': element_validator
            }
        })

        return self

    def __validate_elements(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        validation_success = True
        validation_error = {}
        validated_data = []

        element_validator = attribs.get('element_validator')

        for index, element in enumerate(data):
            validation_result = element_validator.validate(element)
            validation_success = validation_success and validation_result.get(
                'success')
            validated_data.append(validation_result.get('data'))

            if validation_result.get('success') is False:
                validation_error[index] = validation_result.get('error')

        return {
            'success': validation_success,
            'data': validated_data,
            'error': validation_error
        }

    def min(self, min_length, error=None):
        if type(min_length) is not int:
            raise ValueError(
                'value for min_length is expected to be an integer')

        if error is None:
            error = f"At least {min_length} element required."

        self.processors.append({
            'action': self.__assert_min,
            'attribs': {
                'min_length': min_length,
                'error': error
            }
        })

        return self

    def __assert_min(self, data, attribs):
        if data is not None and len(data) < attribs['min_length']:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def max(self, max_length, error=None):
        if type(max_length) is not int:
            raise ValueError(
                'value for max_length is expected to be an integer')

        if error is None:
            error = f"Maximum {max_length} element allowed."

        self.processors.append({
            'action': self.__assert_max,
            'attribs': {
                'max_length': max_length,
                'error': error
            }
        })

        return self

    def __assert_max(self, data, attribs):
        if data is not None and len(data) > attribs['max_length']:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

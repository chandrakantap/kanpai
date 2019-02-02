from .validator import Validator, RequiredMixin


class Array(RequiredMixin, Validator):
    def __init__(self, error="Expecting an array."):
        self.processors = []
        self.processors.append({
            'action': self.__assert_array,
            'attribs': {
                'error': error
            }
        })

    def __assert_array(self, data, attribs):
        if data is None or type(data) is list:
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

from .validator import Validator, RequiredMixin


class Object(RequiredMixin, Validator):

    def __init__(self, schema, error="Expecting an object.", ignore_extra_key=False):
        if type(schema) is not dict:
            raise ValueError('Expecting schema to be a dictionary.')

        for key, validator in schema.items():
            if not isinstance(validator, Validator):
                raise TypeError(f'Expecting a instance of validator in {key}')

        self.processors = []
        self.processors.append({
            'action': self.__assert_data_schema,
            'attribs': {
                'schema': schema,
                'error': error,
                'ignore_extra_key': ignore_extra_key
            }
        })

    def __assert_data_schema(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        if type(data) is not dict:
            return self.validation_error(data, {'data': attribs.get('error')})

        validation_success = True
        validation_data = data
        validation_error = {}

        schema = attribs.get('schema', {})

        for key, validator in schema.items():
            validation_result = validator.validate(data.get(key))
            validation_success = validation_success and validation_result['success']
            validation_data[key] = validation_result['data']
            if validation_result['success'] is False:
                validation_error[key] = validation_result['error']

        if attribs.get('ignore_extra_key') is False:
            for key, value in data.items():
                if schema.get(key) is None:
                    validation_success = False
                    validation_error[key] = f"Unexpected {key}"

        if validation_success is False:
            return self.validation_error(data, validation_error)
        else:
            return self.validation_success(validation_data)

    def assert_equal_field(self, field_one, field_two, error=None):
        if error is None:
            error = f'{field_one} and {field_two} must be same.'
        self.processors.append({
            'action': self.__assert_field_equal,
            'attribs': {
                'field_one': field_one,
                'field_two': field_two,
                'error': error
            }
        })
        return self

    def __assert_field_equal(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        field_one = data.get(attribs.get('field_one'))
        field_two = data.get(attribs.get('field_two'))

        if field_one == field_two:
            return self.validation_success(data)
        else:
            return self.validation_error(data, {attribs.get('field_two'): attribs.get('error')})

from .validator import Validator


class Object(Validator):

    def __init__(self, schema, error="Expecting an object.", ignore_extra_key=False):
        if type(schema) is not dict:
            raise ValueError('Expecting schema to be a dictionary.')

        for key, validator in schema.items():
            if not isinstance(validator, Validator):
                raise TypeError(f'Expecting a instance of validator in {key}')

        self._schema = schema
        self._data_not_object_error = error
        self._ignore_extra_key = ignore_extra_key

    def validate(self, data):
        if type(data) is not dict:
            return self.validation_error(data, {'data': self._data_not_object_error})

        validation_success = True
        validation_data = data
        validation_error = {}

        for key,validator in self._schema.items():
          validation_result = validator.validate(data.get(key))
          validation_success = validation_success and validation_result['success']
          validation_data[key] = validation_result['data']
          if validation_result['success'] is False:
            validation_error[key] = validation_result['error']

        
        if self._ignore_extra_key is False:
          for key,value in data.items():
            if self._schema.get(key) is None:
              validation_success = False
              validation_error[key] = f"Unexpected {key}"

        if validation_success is False:
          return self.validation_error(data,validation_error)
        else:
          return self.validation_success(validation_data)


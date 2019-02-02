from .validator import Validator, RequiredMixin


class Number(RequiredMixin, Validator):

    def __init__(self, error="Value must be a number."):
        self.processors = []
        self.processors.append({
            'action': self.__assert_number,
            'attribs': {
                'error': error
            }
        })

    def __assert_number(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        if type(data) not in (float, int, str):
            return self.validation_error(data, attribs['error'])

        try:
            data = float(data)
            return self.validation_success(data)
        except ValueError:
            return self.validation_error(data, attribs['error'])

    def integer(self):
        self.processors.append({
            'action': self.__convert_to_int,
            'attribs': None
        })

        return self

    def __convert_to_int(self, data, attribs):
        return self.validation_success(data) if data is None else self.validation_success(int(data))

    def between(self, start, end, error=None):
        type_of_start = type(start)
        type_of_end = type(end)

        if type_of_start is not float and type_of_start is not int:
            raise ValueError('Range start must be a number.')

        if type_of_end is not float and type_of_end is not int:
            raise ValueError('Range end must be a number.')

        if error is None:
            error = f"Value must be between {start} and {end}"

        self.processors.append({
            'action': self.__assert_between,
            'attribs': {
                'start': start,
                'end': end,
                'error': error
            }
        })

        return self

    def __assert_between(self, data, attribs):
        if data is None or (data >= attribs.get('start') and data <= attribs.get('end')):
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs.get('error'))

    def max(self, max_value, error=None):
        type_of_max_value = type(max_value)
        if type_of_max_value is not int and type_of_max_value is not float:
            raise ValueError('max_value must be a number.')

        if error is None:
            error = f"Maximum value allowed is {max_value}"

        self.processors.append({
            'action': self.__assert_max,
            'attribs': {
                'max_value': max_value,
                'error': error
            }
        })

        return self

    def __assert_max(self, data, attribs):
        if data is None or data <= attribs.get('max_value'):
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs.get('error'))

    def min(self, min_value, error=None):
        type_of_min_value = type(min_value)
        if type_of_min_value is not int and type_of_min_value is not float:
            raise ValueError('min_value must be a number.')

        if error is None:
            error = f"Minimum value required is {min_value}"

        self.processors.append({
            'action': self.__assert_min,
            'attribs': {
                'min_value': min_value,
                'error': error
            }
        })

        return self

    def __assert_min(self, data, attribs):
        if data is None or data >= attribs.get('min_value'):
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs.get('error'))

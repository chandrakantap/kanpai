from .validator import RequiredMixin


class Boolean(RequiredMixin):
    def __init__(self, error="Value must be a boolean.", extended=False):
        self.extended = extended
        self.processors = []
        self.processors.append({
            'action': self.__assert_boolean,
            'attribs': {
                'error': error
            }
        })

    def __assert_boolean(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        result = None

        if type(data) is bool:
            result = data

        elif self.extended and type(data) is str:
            if data.lower().strip() in('true', 'yes'):
                result = True
            elif data.lower().strip() in ('false', 'no'):
                result = False

        elif self.extended and type(data) is int:
            if data == 0:
                result = False
            else:
                result = True

        if result is None:
            return self.validation_error(data, attribs['error'])

        return self.validation_success(result)

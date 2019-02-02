from .validator import Validator, RequiredMixin
from uuid import UUID as pyUUID


class UUID(RequiredMixin, Validator):

    def __assert_uuid(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        try:
            return self.validation_success(pyUUID(data))
        except Exception:
            return self.validation_error(data, attribs['error'])

    def __init__(self, error='Value must be a of type UUID'):
        self.processors = []
        self.processors.append({
            'action': self.__assert_uuid,
            'attribs': {
                'error': error
            }
        })

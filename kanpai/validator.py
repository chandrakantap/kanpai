class Validator(object):

    def validation_error(self, data, error):
        return {
            'success': False,
            'data': data,
            'error': error
        }

    def validation_success(self, data):
        return {
            'success': True,
            'data': data,
            'error': None
        }

    def validate(self, data):
        last_processor_result = {
            'data' : data
        }

        for processor in self.processors:
            last_processor_result = processor['action'](
                last_processor_result['data'], processor['attribs'])

            if last_processor_result['success'] is False:
                break

        if last_processor_result['success'] is False:
            return self.validation_error(data,last_processor_result['error'])
        else:
            return last_processor_result

from .string import String


class Email(String):

    def __init__(self, error="Email must be a string"):
        super().__init__(error=error)
        super().match(r'[^@]+@[^@]+\.[^@]+')

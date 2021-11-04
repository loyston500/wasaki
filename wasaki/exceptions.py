class AlreadyRegisteredError(Exception):
    pass


class ConversionError(Exception):
    pass


class InvalidEventError(Exception):
    pass


class NotRegisteredError(Exception):
    pass


class EventNotRegisteredError(NotRegisteredError):
    pass


class CommandNotRegisteredError(NotRegisteredError):
    pass

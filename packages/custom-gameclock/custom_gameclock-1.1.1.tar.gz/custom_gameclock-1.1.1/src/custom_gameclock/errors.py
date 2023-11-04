'''Errors used in the gameclock'''

class TimestampError(ValueError):
    '''Timestamp Error'''

class FormattingError(ValueError):
    '''Formatting Error'''

class EnumError(ValueError, TypeError):
    '''Enum Error'''

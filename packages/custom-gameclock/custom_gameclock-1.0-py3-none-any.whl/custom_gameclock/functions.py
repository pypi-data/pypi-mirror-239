# pylint: disable=too-many-arguments, trailing-whitespace
'''
Miscellaneous functions used in the gamclock package.
'''

from typing import Any, TYPE_CHECKING

from . import vocabulary as vcb
if TYPE_CHECKING:
    from .formatting import CalendarLimits, CalendarTimestamp


def get_dict_canon(prototype: dict[str, Any]) -> dict[str, type]:
    '''
    Return the given dictionary with the values replaced by the values' types.
    '''
    return {key: type(value) for key, value in prototype.items()}


def compare_dict_value_types(first: dict[str, Any], second: dict[str, Any]) -> bool:
    '''
    Return True if the keys and value types of two dictionaries are the same.
    '''
    return get_dict_canon(first) == get_dict_canon(second)


def quick_limits(leap_month: str = '', 
                 leap_year_frequency: int = 0, 
                 minutes_in_hour: int = 0,
                 hours_in_day: int = 0, 
                 days_in_month: dict[str, int] | None = None) -> 'CalendarLimits':
    '''
    Shortcut to get properly formatted CalendarLimits.
    '''
    if days_in_month is None:
        days_in_month = {}

    limits: CalendarLimits = {
        'leap_month': leap_month,
        'leap_year_frequency': leap_year_frequency,
        'minutes_in_hour': minutes_in_hour,
        'hours_in_day': hours_in_day,
        'days_in_month': days_in_month
    }

    return limits


def quick_timestamp(minutes: int, 
                    hours: int, 
                    day_of_week: str, 
                    month: str,
                    year: int, 
                    leap_year: int, 
                    day_of_month: int) -> 'CalendarTimestamp':
    '''
    Shortcut to get properly formatted CalendarTimestamp.
    '''
    timestamp: CalendarTimestamp = {
        vcb.MINUTES: minutes,
        vcb.HOURS: hours,
        vcb.DAY_OF_WEEK: day_of_week,
        vcb.MONTH: month,
        vcb.DAY_OF_MONTH: day_of_month,
        vcb.YEAR: year,
        vcb.LEAP_YEAR: leap_year
    }

    return timestamp

# pylint: disable=trailing-whitespace, trailing-newlines, too-many-instance-attributes
'''
Formatting data that the clock needs to function. We allow for custom clock
systems defined by the enums Days and Months, which are alongside a dictionary
of basic constants for the clock's operation. These basic constants can be 
input using a pre-defined CalendarConstants TypedDict for easy typing, but
this is not necessary since it will be treated as a plain dictionary at
runtime.
'''

from typing import TypedDict
from dataclasses import dataclass, field
from enum import StrEnum

from .mixins import EnumSequenceMixin
from .errors import EnumError
from .functions import compare_dict_value_types, quick_limits
from . import vocabulary as vcb


class Days(EnumSequenceMixin, StrEnum):
    '''Enum for creating custom sets of weekday names.
    
    Simply create a custom range of day names using
    enum.auto, pass them along with the setup data, 
    (see Calendar class) and the clock will use those
    names instead of Monday, Tuesday, etc. You can use 
    any number of days to make up the weeks.

    Example:

        from enum import auto

        class FantasyGameDays(Days):
            SUNNENGAR = auto()
            BROBLESTAM = auto()
            MALLENHAR = auto()
            RAGGENSACK = auto()

    This can be used to make custom date-times like:

         HH:MM, Days      Months  DD  YYYY
        '33:87, sunnegar, mordoch 45, 6675'
    '''


class Months(EnumSequenceMixin, StrEnum):
    '''Enum for creating custom sets of month names.
    
    Simply create a custom range of month names using
    enum.auto, pass them along with the setup data, 
    (see Calendar class) and the clock will use those
    names instead of January, February, etc. You can use 
    any number of months to make up the year.

    Example:

        from enum import auto

        class FantasyGameMonths(Months):
            MORDOCH = auto()
            KELLENCRAT = auto()
            SENIGAFI = auto()
            MORENTAR = auto()
            PAPALAMUN = auto()
            GRIZMOROCK = auto()

    This can be used to make custom date-times like:

         HH:MM, Days      Months  DD  YYYY
        '33:87, sunnegar, mordoch 45, 6675'
    '''
    

class CalendarLimits(TypedDict):
    '''
    Defines the limits of the calendar.

    Values:
        leap_month : str
        leap_year_frequency : int
        minutes_in_hour : int
        hours_in_day : int
        days_in_month : dict[str, int]
    '''
    leap_month: str
    leap_year_frequency: int
    minutes_in_hour: int
    hours_in_day: int
    days_in_month: dict[str, int]


class CalendarTimestamp(TypedDict):
    '''
    Information that serves as a timestamp.

    Values:
        minutes : int
        hours : int
        year : int 
        month : str
        day_of_month : int
        day_of_week : str
        leap_year : int
    '''
    minutes: int
    hours: int
    year: int
    month: str
    day_of_month: int
    day_of_week: str
    leap_year: int


@dataclass
class CalendarFormatting():
    '''
    This class is a container for the constants the clock uses.

    We make custom calendar names with the packaged enums ``gameclock.Days`` and
    ``gameclock.Months``, along with a dictionary of basic constant values in 
    the same structure as the ``gameclock.CalendarLimits`` TypedDict. This class
    does a little bit of validation to make sure that the basic constants of
    the calendar are not contradictory in some way.


    Parameters
    ----------
    limits : CalendarLimits
        The basic limits of minutes in an hour, hours in a day, etc.
    days_in_week : Days
        The names of days in order.
    months_in_year : Months
        The names of months in order.

    Raises
    ------
    TypeError
        If one of the values in the CalendarLimits is of the wrong data type.
    EnumError
        If the days_in_week, months_in_year are not the Days, Months enums.
    '''
    limits: CalendarLimits
    days_in_week: type[Days]
    months_in_year: type[Months]
    leap_month:str = field(init=False)
    leap_year_frequency:int = field(init=False)
    hours_in_day:int = field(init=False)
    days_in_month:dict[str, int] = field(init=False)
    minutes_in_hour:int = field(init=False)
    days_in_year:int = field(init=False)


    def __post_init__(self):
        if not compare_dict_value_types(dict(quick_limits()), dict(self.limits)):
            raise TypeError(self.limits)

        if not issubclass(self.months_in_year, Months) or not issubclass(self.days_in_week, Days):
            raise EnumError('Must use custom enums Months and Days.')

        if list(self.months_in_year) != list(self.limits[vcb.DAYS_IN_MONTH].keys()):
            raise EnumError('Month enum is not synchronizd with days_in_month dictionary.', [
                            month.name for month in self.months_in_year], list(self.limits.keys()))

        self.__setattr__('leap_month', self.limits[vcb.LEAP_MONTH])
        self.__setattr__('hours_in_day', self.limits[vcb.HOURS_IN_DAY])
        self.__setattr__('minutes_in_hour', self.limits[vcb.MINUTES_IN_HOUR])
        self.__setattr__('days_in_month', self.limits[vcb.DAYS_IN_MONTH])
        self.__setattr__('leap_year_frequency',
                         self.limits[vcb.LEAP_YEAR_FREQUENCY])
        self.__setattr__('days_in_year', sum(
            days for days in self.limits[vcb.DAYS_IN_MONTH].values()))


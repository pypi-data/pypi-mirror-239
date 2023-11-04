'''Default values used in the gameclock.'''
from enum import auto, Enum
from typing import cast
from . import vocabulary as vcb
from .formatting import CalendarFormatting, CalendarLimits, Days, Months


class Speeds(float, Enum):
    '''
    Sugestions for setting the speed of the game clock.

    The clock is controlled by an external loop calling
    `GameClock().tick()`, so these values have no role in
    the internal operation of the GameClock class.
    ::   

                Minutes         Hours       Days
              ---------------------------------------
    VERY_SLOW | 1s      = 1m    1m   = 1h   24m  = 1d
    SLOW      | 0.5s    = 1m    30s  = 1h   12m  = 1d
    NORMAL    | 0.25s   = 1m    15s  = 1h   6m   = 1d
    FAST      | 0.058s  = 1m    3.5s = 1h   1m   = 1d
    VERY_FAST | 0.016s  = 1m    1s   = 1h   24s  = 1d
    '''
    VERY_SLOW = 1.0
    SLOW = 0.5
    NORMAL = 0.25
    FAST = 0.058
    VERY_FAST = 0.016


class EnglishDays(Days):
    '''
    Default day names.
    '''
    SUNDAY = auto()
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()


class EnglishMonths(Months):
    '''
    Default month names.
    '''
    JANUARY = auto()
    FEBRUARY = auto()
    MARCH = auto()
    APRIL = auto()
    MAY = auto()
    JUNE = auto()
    JULY = auto()
    AUGUST = auto()
    SEPTEMBER = auto()
    OCTOBER = auto()
    NOVEMBER = auto()
    DECEMBER = auto()


ENGLISH_CALENDAR_DATA: dict[str, int|str|dict[str,int]]= {
    vcb.LEAP_MONTH:'february',
    vcb.LEAP_YEAR_FREQUENCY: 4,
    vcb.MINUTES_IN_HOUR: 60,
    vcb.HOURS_IN_DAY: 24,
    vcb.DAYS_IN_MONTH:{
        'january':31, 
        'february':28, 
        'march':31, 
        'april':30, 
        'may':31, 
        'june':30, 
        'july':31, 
        'august':31, 
        'september':30, 
        'october':31, 
        'november':30, 
        'december':31
        }
    }


DEFAULT_CALENDAR_LIMITS: CalendarLimits = cast(CalendarLimits, ENGLISH_CALENDAR_DATA)

DEFAULT_FORMATTING: CalendarFormatting = CalendarFormatting(DEFAULT_CALENDAR_LIMITS,
                                                         EnglishDays,
                                                         EnglishMonths)

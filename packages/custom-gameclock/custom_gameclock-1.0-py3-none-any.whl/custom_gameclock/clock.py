# pylint: disable=trailing-whitespace, trailing-newlines, too-many-instance-attributes
'''
The main GameClock class.

The game clock can accommodate irregular calendar cycles and custom day 
and month names, but also supports the English Gregorian calendar as a 
default. The use of leap years is not mandatory; if leap years are used,
the (non-)skipping of centurial leap years is hard-coded at (400) 100.
'''

from typing import cast

from .functions import compare_dict_value_types
from .formatting import CalendarFormatting, CalendarTimestamp
from .errors import TimestampError
from . import vocabulary as vcb
from .defaults import DEFAULT_FORMATTING

class GameClock:
    '''
    A clock to represent the amount of game time that has passed.

    Parameters
    ----------
    calendar_formatting : CalendarFormatting, optional
        A properly-formatted instance of ``gameclock.CalendarFormatting``
        (see that class' doc for more details). If not specified, the English
        Gregorian calendar will be used.

    starting_time : CalendarTimestamp, optional
        The time at which the clock will start. If not specified, the default
        starting time will be used.

    Methods
    -------
    tick :  None
        Advance the clock by 1 minute
    prettytime :  str
        Return e.g.: 'HH:MM, DAYNAME, MONTHNAME, DD, YYYY'.
    current_time : dict
        Dictionary timestamp of current time.
    set_time : None
        Set clock time using dictionary timestamp.
    get_total_minutes : int
        Calculate the number of minutes in a timestamp.
    get_alarm : int
        Get an int representing current time + n minutes.
    alarm_done : bool
        Check whether current time is later than the alarm.

    Examples
    --------
    >>> cal = GameClock()
    >>> cal.tick()
    >>> cal.tick()
    >>> cal.tick()
    >>> cal.prettytime()
    '00:03, Sunday, January 1, 1'

    The gameclock defaults to Gregorian time without further need for 
    configuration.
    '''
    
    # /-------------------------------NOTES----------------------------------/
    #
    # TODO: The clock requires a 'leap month' even if leap_year_frequency is
    # set to 0 (i.e. no leap years). 
    #
    # TODO: The class can calculate the minutes from a timestamp, but not a
    # timestamp from the minutes.
    #
    # /----------------------------------------------------------------------/

    def __init__(self,
                 calendar_formatting: CalendarFormatting | None = None,
                 starting_time: CalendarTimestamp | None = None
                 ):

        # Basic cycles of time that will be counted. Since the game clock
        # runs in dilated time, we consider minutes to be the smallest unit.
        self.minutes: int
        self.hours: int
        self.day_of_week: str
        self.day_of_month: int
        self.month: str
        self.year: int
        self.leap_year: int

        # Formatting constants: allows for custom date ranges.
        # The clock cannot do anything without the formatting being set first.
        self.__constants: CalendarFormatting = calendar_formatting or DEFAULT_FORMATTING

        # Validate and set the starting time of the clock.
        time: CalendarTimestamp = starting_time or self.default_time
        
        if not self.__check_timestamp_compatibility(time):
            raise TimestampError(
                f'Timestamp {time} is incompatible with the given formatting.')
        self.set_time(time)


    @property
    def default_time(self) -> CalendarTimestamp:
        '''
        Returns the default time in a dictionary conforming to the formatting 
        defined in the CalendarTimestamp TypedDict.
        '''
        timestamp = {
            vcb.MINUTES: 0,
            vcb.HOURS: 0,
            vcb.DAY_OF_WEEK: self.__constants.days_in_week.define_first(),
            vcb.DAY_OF_MONTH: 1,
            vcb.YEAR: 1,
            vcb.LEAP_YEAR: 0,
            vcb.LEAP_YEAR_FREQUENCY: 1,
            vcb.MONTH: self.__constants.months_in_year.define_first()
        }
        return cast(CalendarTimestamp, timestamp)
    

    def convert_minutes_to_timestamp(self, minutes: int) -> CalendarTimestamp:
        '''
        Use the formatting to generate a timestamp from the given number of minutes.
        '''        
        minutes +=1 
        # placeholder


        return self.default_time


    def get_total_minutes(self, time: CalendarTimestamp) -> int:
        '''
        Calculate the total number of minutes in a timestamp.

        Return an integer representing the total number of minutes since 
        the default time of the class: 

            00:00 days_in_week[0], months_in_year[0] 1, 1

        In the default formatting, this is equivalent to:

            00:00 Sunday, January 1, 1 

        Parameters
        ----------
        time : CalendarTimestamp
            A timestamp with the same formatting as the class.

        Returns
        -------
        int
            The total number of minutes, allowing for leapyears and so on.
        '''
        total: float = 0.0
        if not self.__check_timestamp_compatibility(time):
            raise ValueError(time)

        hrs = self.__constants.hours_in_day
        mins = self.__constants.minutes_in_hour
        yrs = self.__constants.days_in_year

        # Invariant calculations
        # ----------------------
        total += time[vcb.MINUTES]
        total += (time[vcb.YEAR] - 1) * yrs * hrs * mins  # minus 1 for no year 0
        total += (time[vcb.DAY_OF_MONTH] - 1) * hrs * mins  # minus 1 for no day 0
        total += time[vcb.HOURS] * mins

        # Variant calculations
        # --------------------

        # Months
        months = [month.value for month in self.__constants.months_in_year]
        months = months[:months.index(time[vcb.MONTH])]
        for month in months:
            total += self.__constants.days_in_month[month] * hrs * mins

        # Leap years
        leap_days = 0
        if time[vcb.YEAR] >= self.__constants.leap_year_frequency and self.__constants.leap_year_frequency != 0:
            leap_days = int(
                time[vcb.YEAR] / self.__constants.leap_year_frequency) * hrs * mins

        # Remove the portion of a leap day that has already elapsed
        offset = 0
        if time[vcb.LEAP_YEAR] == self.__constants.leap_year_frequency:
            offset = 1 * hrs * mins
        total += leap_days - offset

        # Calculate centurial leap years (skip leap year every 100 years, but 
        # not every 400 years).
        subtract = 0
        add = 0
        if time[vcb.YEAR] / 100 > 1:
            subtract = time[vcb.YEAR] // 100 * hrs * mins
        if time[vcb.YEAR] / 400 > 1:
            add = time[vcb.YEAR] // 400 * hrs * mins
        total += add
        total -= subtract    

        return int(total)


    def tick(self) -> None:
        '''
        Advance the clock by 1 of the smallest unit.
        '''
        self.__next_minute()


    @property
    def prettytime(self) -> str:
        '''
        Return a nicely-formatted string of the current time (won't work as a timestamp).
        '''
        return f'{self.hours:02}:{self.minutes:02} - {self.day_of_week.capitalize()}, {self.month.capitalize()} {self.day_of_month}, {self.year}'


    @property
    def current_time(self) -> CalendarTimestamp:
        '''
        Return the current time in a dictionary format.
        '''
        return {'minutes': self.minutes,
                'hours': self.hours,
                'day_of_week': self.day_of_week,
                'month': self.month,
                'day_of_month': self.day_of_month,
                'year': self.year,
                'leap_year': self.leap_year}


    def get_alarm(self, minutes: int) -> int:
        '''
        Return the current absolute number of minutes + the given timer.
        '''
        return self.get_total_minutes(self.current_time) + minutes


    def alarm_done(self, alarm: int) -> bool:
        '''
        Check if an alarm is done.
        '''
        return alarm <= self.get_total_minutes(self.current_time)


    def set_time(self, starting_point: CalendarTimestamp) -> None:
        '''
        Set the clock to the time represented by the input dictionary.
        '''
        self.minutes: int = starting_point[vcb.MINUTES]
        self.hours: int = starting_point[vcb.HOURS]
        self.day_of_week: str = starting_point[vcb.DAY_OF_WEEK]
        self.day_of_month: int = starting_point[vcb.DAY_OF_MONTH]
        self.month: str = starting_point[vcb.MONTH]
        self.year: int = starting_point[vcb.YEAR]
        self.leap_year: int = starting_point[vcb.LEAP_YEAR]


    def __next_value(self, current_value: int, max_value: int) -> int:
        '''
        Rolls over values if they are about to reach the maximum.
        '''
        return 0 if current_value + 1 >= max_value else current_value + 1


    def __next_minute(self) -> None:
        '''
        Advance to the next minute in the minute cycle.
        '''
        # Currently, this is the smallest unit of time.
        self.minutes = self.__next_value(
            self.minutes, self.__constants.minutes_in_hour)
        if self.minutes == 0:
            self.__next_hour()


    def __next_hour(self) -> None:
        '''
        Advance to the next hour in the hour cycle.
        '''
        self.hours = self.__next_value(
            self.hours, self.__constants.hours_in_day)
        if self.hours == 0:
            self.__next_day()


    def __get_month_length(self) -> int:
        '''
        Helper function to decide how many days the month gets.
        '''
        # Is it leap year?
        if self.month == self.__constants.leap_month and self.leap_year + 1 == self.__constants.leap_year_frequency:
            # Is it time to skip a leap year?
            if self.year % 100 == 0:
                month_length = self.__constants.days_in_month[self.__constants.leap_month]
                if self.year % 400 == 0:
                    month_length += 1
            else:
                month_length = self.__constants.days_in_month[self.__constants.leap_month] + 1
        else:
            month_length = self.__constants.days_in_month[self.month]
        return month_length


    def __next_day(self) -> None:
        '''
        Advance the next day, both in the day/week cycle, and the day/month cycle.
        '''
        self.day_of_week = str(
            self.__constants.days_in_week.cycle_next(self.day_of_week))
        # Check month rollover
        if self.day_of_month == self.__get_month_length():
            # Check leapyear rollover
            if self.month == self.__constants.leap_month:
                self.__next_leap_year()
            self.day_of_month = 1
            self.__next_month()
        else:
            self.day_of_month += 1


    def __next_leap_year(self) -> None:
        '''
        Advance to the next year in the leapyear cycle.
        '''
        self.leap_year = self.__next_value(
            self.leap_year, self.__constants.leap_year_frequency)


    def __next_month(self) -> None:
        '''
        Advance to the next month in the month cycle.
        '''
        self.month = str(
            self.__constants.months_in_year.cycle_next(self.month))
        if self.__constants.months_in_year.is_first(self.month):
            self.__next_year()


    def __next_year(self) -> None:
        '''
        Advance to the next year.
        '''
        self.year += 1


    def __check_timestamp_compatibility(self, timestamp: CalendarTimestamp) -> bool:
        '''
        Check for any sign that the timestamp is from a different calendar 
        system than the current calendar system, which might prevent the 
        functioning of the clock.
        '''
        if not compare_dict_value_types(dict(self.default_time), dict(timestamp)):
            return False
        if timestamp[vcb.DAY_OF_WEEK] not in [x for x in self.__constants.days_in_week]:
            return False
        if timestamp[vcb.MONTH] not in [x for x in self.__constants.months_in_year]:
            return False
        if timestamp[vcb.MINUTES] > self.__constants.minutes_in_hour or timestamp[vcb.HOURS] > self.__constants.hours_in_day:
            return False
        return True

=================
Custom Game Clock
=================

.. contents::

Installation
------------

``py -m pip install custom-gameclock``


Description
-----------
The custom game clock package provides a simple, customizable clock/calendar for use in a
video game. The clock is controlled by calling the ``GameClock().tick()`` method,
and the user is responsible for ensuring that the method is called at an appropriate interval and with correct timing.

Usage
-----
The clock will keep time based on user-defined calendar systems, which are wrapped in a CalendarFormatting object. This allows the clock to track
calendars with different month and day names, as well as different numbers of days, months, hours, etc. compared to the English Gregorian calendar.

Simple, easy, out-of-the-box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the user doesn't need a customized calendar, then ``GameClock()`` will return a calendar formatted to the English Gregorian system. 

.. code:: Python

    import time
    from custom_gameclock import GameClock, Speeds

    clock = GameClock()
    running = True
    while running:
        clock.tick()
        print(clock.prettytime)
        time.sleep(Speeds.NORMAL)

This example uses the standard library ``time`` to call ``GameClock().tick()`` at regular intervals (in a precariously uncontrolled loop), but the user can customize the main loop in whatever
way is desired. The included ``Speeds`` enum has some suggestions in miliseconds.

The clock starts at a default time in the example above, but we can pass a dictionary timestamp during initialization to set the starting time. If we're using the default
calendar formatting, like above, then the starting timestamp must be passed as a keyword argument. 

.. code:: Python
    
    from custom_gameclock import GameClock
    clock = GameClock(starting_time={'month':'january', 
                                     'day_of_month':4, 
                                     'day_of_week':'monday',
                                     'minutes': 33,
                                     'hours': 6,
                                     'year': 1995
                                     'leap_year': 3})

Oops! We set the clock to a date that doesn't exist! If we want to change the clock's time after initialization, we can use the ``GameClock().set_time`` method:

.. code:: Python

    clock.set_time({'month':'january', 
                    'day_of_month':4, 
                    'day_of_week':'monday',
                    'minutes': 33,
                    'hours': 6,
                    'year': 1993
                    'leap_year': 3})

If we had kept the starting time we originally set, the clock itself would have worked fine, but it would have been unable to resolve timestamps into integers and back again properly.
This means that the timing system (see further below) would have generated incorrect alarms.

Display
+++++++

Nicely-formatted time is returned from the ``GameClock().prettytime`` property, and
a plain dictionary timestamp is returned from the ``GameClock().current_time`` property:

.. code:: Python

    >>> from custom_gameclock import GameClock
    >>> x = GameClock()
    >>> x.prettytime
    '00:00 - Sunday, January 1, 1'
    >>> x.current_time
    {'minutes': 0, 'hours': 0, 'day_of_week': 'sunday', 'month': 'january', 'day_of_month': 1, 'year': 1, 'leap_year': 0}

Timers
++++++

The clock can also set an alarm for a certain number of ticks from the current time. Use the ``GameClock().get_alarm()`` method to 
get an alarm, and pass the alarm (dictionary timestamp) to ``GameClock().alarm_done()`` to test whether the alarm is done yet.

The alarms work by calculating the total number of minutes elapsed since the clock's default time and comparing them between two timestamps.
If you want to convert a timestamp to total minutes, you can pass a properly-formatted timestamp to the ``GameClock().get_total_minutes(timestamp)`` method too.

.. code:: Python

    >>> from custom_gameclock import GameClock
    >>> x = GameClock()
    >>> alarm = x.get_alarm(50000)
    >>> while x.alarm_done(alarm) is False:
    ...     x.tick()
    >>> print('Alarm done!', x.prettytime)
    Alarm done! 17:20 - Saturday, February 4, 1
    >>> timestamp = x.current_time
    >>> x.get_total_minutes(timestamp)
    50000

Note: The calculation of total minutes assumes that the planet skips a leap year every 100 years, but not every 400 years. This is borrowed from the Gregorian calendar
and is hard-coded into the calculation (for now). Any custom calendar that uses leap years will observe this pattern. If you want to avoid using 
leap years entirely, simply set ``leap_year_frequency`` to ``0`` in the dictionary of calendar limits wrapped in the ``CalendarFormatting`` class, outlined below.


Custom Calendars
~~~~~~~~~~~~~~~~

Custom calendar systems are supported by passing an instance of the ``CalendarFormatting`` class when initializing
the clock. This class serves as a wrapper (with a little validation) for the basic constants the clock uses.

Days and Months
+++++++++++++++
The ``Days`` and ``Months`` enums are used to define the names of the days and months that the calendar will use.
Any names can be used, as long as they are unique in their enum. 

CalendarFormatting
++++++++++++++++++
The ``CalendarFormatting`` class is initialized with a dictionary of limits, as well as the ``Days`` and ``Months`` enums.
This dictionary defines the points at which different units of time will roll over into the next unit.
The class checks that the names of the months are the same as those in the ``Months`` enum, and that the leap month is a valid name.

.. code:: Python

    from enum import auto
    from gameclock import GameClock, Days, Months, CalendarFormatting

    values = {'leap_month': 'winter', 
              'leap_year_frequency': 3, 
              'minutes_in_hour': 100, 
              'hours_in_day': 14, 
              'days_in_month': {'spring': 28, 
                               'summer': 28, 
                               'fall': 28, 
                               'winter': 28}
              }

    class FantasyGameMonths(Months):
        SPRING = auto()
        SUMMER = auto()
        FALL = auto()
        WINTER = auto()

    class FantasyGameDays(Days):
        MORDOCH = auto()
        KELLENCRAT = auto()
        DRAGGENTHAR = auto()

    cal = CalendarFormatting(values, FantasyGameDays, FantasyGameMonths)

    starting_time = {'minutes': 66, 
                     'hours': 12, 
                     'year': 33, 
                     'month': 'winter', 
                     'day_of_month': 24, 
                     'day_of_week': 'draggenthar', 
                     'leap_year': 3}

    clock = GameClock(cal, starting_time)

Now the clock is formatted to use the custom calendar:

.. code:: Python

    >>> clock.prettytime
    '12:66 - Draggenthar, Winter 24, 33'


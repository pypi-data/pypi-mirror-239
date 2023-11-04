'''
Mixins used in the package.
'''
from enum import Enum
from random import choice
from .vocabulary import NEXT, PREVIOUS, LINEAR, CIRCULAR


class EnumSequenceMixin(Enum):
    '''
    Mixin to allow a user to sequence the values of an enum.

    This class is used as a parent class along with an ``IntEnum`` or ``StrEnum`` 
    in order to add methods that allow us to get the next or previous value
    of an enum in a circular or linear order. 
    
    Use ``enum.auto`` to define the values. The order of values in the enum
    is the definition order. 

    Examples
    --------
    >>> Elements(EnumSequenceMixin, StrEnum):
    ... EARTH = auto()
    ... WATER = auto()
    ... AIR = auto()
    ... FIRE = auto()
    ... AETHER = auto()

    >>> Elements.next_value(Elements.WATER)
    'air'

    >>> Elements.next_value('water')
    'air'

    >>> Elements.next_value(Elements.AETHER)
    'aether'

    >>> Elements.previous_value(Elements.WATER)
    'earth'

    >>> Elements.cycle_next(Elements.AETHER)
    'earth'

    >>> Elements.cycle_previous(Elements.EARTH)
    'aether'

    >>> x = Elements.random()
    >>> x in Elements.get_all()
    True

    >>> Elements.define_last()
    'aether'

    >>> Elements.define_first()
    'earth'

    >>> Elements.is_first('water')
    False
    '''

    @classmethod
    def get(cls, current_value:int|str, direction:str=NEXT, sequence:str=LINEAR) -> str|int:
        '''
        Generically fetch the next or previous value.
        
        The linear sequence will keep returning the same value when either
        limit of the scale is reached. The circular sequence will treat the
        last and first values as adjacent.
        
        Parameters
        ----------
        current_value : int | str
            The value to be compared.
        direction : str, optional
            The direction of order, by default NEXT
        sequence : str, optional
            The type of order, by default LINEAR

        Returns
        -------
        str|int
            The requested value from the enum.
        '''
        cls.__validate(current_value, direction, sequence)
        values = cls.get_all()
        value = current_value

        if direction == NEXT:
            if cls.is_last(current_value):
                if sequence == LINEAR:
                    pass
                elif sequence == CIRCULAR:
                    value = cls.define_first()
            else:
                value = values[values.index(current_value) + 1]

        elif direction == PREVIOUS:
            if cls.is_first(current_value):
                if sequence == LINEAR:
                    pass
                elif sequence == CIRCULAR:
                    value = cls.define_last()
            else:
                value = values[values.index(current_value) - 1]

        return value


    # / ----------------------------SHORTCUT METHODS-------------------------/
    @classmethod
    def next_value(cls, current_value:int|str) -> int|str:
        '''
        Returns the next value in the definition order, or the last value if 
        the given value is already last.
        '''
        return cls.get(current_value)


    @classmethod
    def previous_value(cls, current_value:int|str) -> int|str:
        '''
        Returns the previous value in the definition order, or the first 
        value if the given value is already first.
        '''
        return cls.get(current_value, PREVIOUS)


    @classmethod
    def cycle_next(cls, current_value:int|str) -> int|str:
        '''
        Returns the next value in the definition order, or returns the first 
        value if there is no next.
        '''
        return cls.get(current_value, sequence=CIRCULAR)
    

    @classmethod
    def cycle_previous(cls, current_value:int|str) -> int|str:
        '''
        Returns the previous value in the definition order, or the last value 
        if there is no previous.
        '''
        return cls.get(current_value, PREVIOUS, CIRCULAR)


    # /----------------------------AUXILIARY METHODS-------------------------/
    @classmethod
    def is_last(cls, current_value:int|str) -> bool:
        '''
        Return True if the provided value is last in the enum.
        '''
        return current_value == cls.define_last()


    @classmethod
    def is_first(cls, current_value:int|str) -> bool:
        '''
        Return True if the provided value is first in the enum.
        '''
        return current_value == cls.define_first()


    @classmethod
    def define_last(cls) -> str|int:
        '''
        Return the value of the last item in the enum's definition order.
        '''
        return cls.get_all()[-1]


    @classmethod
    def define_first(cls) -> str|int:
        '''
        Return the value of the first item in the enum's definition order.
        '''
        return cls.get_all()[0]


    @classmethod
    def get_random(cls) -> str|int:
        '''
        Call random.choice on the values of the enum.
        '''
        return choice(cls.get_all())


    @classmethod
    def get_all(cls) -> list[str|int]:
        '''
        Return all values in the enum.
        '''
        return [item.value for item in cls]
    

    @classmethod
    def __validate(cls, current_value:int|str, direction:str, sequence: str):
        '''
        Raise an error if any the request data is incompatible.
        '''
        if direction not in [NEXT, PREVIOUS]:
            raise ValueError(direction)
        if sequence not in [LINEAR, CIRCULAR]:
            raise ValueError(sequence)
        if current_value not in cls.get_all():
            raise ValueError(current_value)
        
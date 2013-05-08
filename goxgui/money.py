from currency import Currency


class Money(object):
    '''
    Represents a money value including various attributes
    such as currency type, number of decimals to render, etc.
    '''
    __INTERNAL_DECIMALS = 8
    __INTERNAL_FACTOR = pow(10, __INTERNAL_DECIMALS)

    def __init__(self, value=0, currency=Currency('BTC'), shift=True):

        if shift:
            self.__value = long(value * Money.__INTERNAL_FACTOR)
        else:
            self.__value = long(value)

        self.__currency = currency
        self.__symbol = ''

    def __str__(self):
        '''
        Returns the current money value as a string.
        '''
        return '{{:,.{}f}}'.format(self.decimals).format(self.to_float())

    def to_long_string(self):
        '''
        Returns the current money value as a string including currency type
        '''
        return '{} {}'.format(self.__str__(), self.__currency)

    def to_float(self):
        '''
        Returns the money value as a float.
        '''
        return self.value / float(Money.__INTERNAL_FACTOR)

    def __mul__(self, other):
        '''
        Multiplies the current money value with the specified other
        money value. The result will have the currency of the current value.
        '''
        return Money(self.value * other.value / Money.__INTERNAL_FACTOR,
            self.currency, False)

    def __div__(self, other):
        '''
        Divides the current money value by the specified other money value.
        The result will have the currency of the current value.
        '''
        return Money(self.value * Money.__INTERNAL_FACTOR / other.value,
            self.currency, False)

    def __add__(self, other):
        '''
        Adds another money value to this one.
        The resulting money value will have the same type as this one.
        '''
        return Money(self.value + other.value, self.currency, False)

    def __sub__(self, other):
        '''
        Subtracts another money value from this one.
        The resulting money value will have the same type as this one.
        '''
        return Money(self.value - other.value, self.currency, False)

    def pip(self):
        '''
        Returns a money value that is the equivalent of one pip.
        '''
        return Money(pow(10, -self.decimals), self.currency)

    def get_currency(self):
        return self.__currency

    def set_currency(self, currency):
        self.__currency = currency

    def get_value(self):
        return self.__value

    def get_decimals(self):
        return self.__currency.decimals

    def get_symbol(self):
        return self.__currency.symbol

    currency = property(get_currency, set_currency, None, None)
    value = property(get_value, None, None, None)
    decimals = property(get_decimals, None, None, None)
    symbol = property(get_symbol, None, None, None)

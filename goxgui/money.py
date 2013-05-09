

INTERNAL_DECIMALS = 8
INTERNAL_FACTOR = pow(10, INTERNAL_DECIMALS)


def to_string(value, currency):
    '''
    Returns the current money value as a string.
    '''
    return '{{:,.{}f}}'.format(currency.decimals).format(to_float(value))


def to_long_string(value, currency):
    '''
    Returns the value as a string including currency type.
    '''
    return '{} {}'.format(to_string(value, currency), currency)


def to_money(value):
    '''
    Returns the float value as a money value
    '''
    return long(value * INTERNAL_FACTOR)


def to_float(value):
    '''
    Returns the money value as a float.
    '''
    return value / float(INTERNAL_FACTOR)


def multiply(valueA, valueB):
    '''
    Multiplies the money value with money value B
    '''
    return valueA * valueB / INTERNAL_FACTOR


def divide(valueA, valueB):
    '''
    Divides monyey value A by money value B
    '''
    return valueA * INTERNAL_FACTOR / valueB


def pip(currency):
    '''
    Returns a money value that is the equivalent of
    one pip given the specified currency.
    '''
    return pow(10, INTERNAL_DECIMALS - currency.decimals)

class Currency(object):
    '''
    Represents a currency.
    '''

    # The amount of decimals is used when rendering the currency.
    # Also used to determine the size of a pip.
    # All currencies not listed here will have 5 decimals.
    __DECIMALS = {
        'BTC': 8,
        'JPY': 3,
        'SEK': 3,
        }

    def __init__(self, symbol):

        if symbol in self.__DECIMALS:
            self.__decimals = Currency.__DECIMALS[symbol]
        else:
            self.__decimals = 5

        self.__symbol = symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def get_symbol(self):
        return self.__symbol

    def get_decimals(self):
        return self.__decimals

    def __str__(self):
        return self.symbol

    symbol = property(get_symbol, None, None, None)
    decimals = property(get_decimals, None, None, None)

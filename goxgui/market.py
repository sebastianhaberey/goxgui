import goxapi
import time

from preferences import Preferences
from currency import Currency
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal
from money import Money


class Market(QObject):
    '''
    Wrapper for gox object used to decouple gui code
    from market implementation.
    '''

    # all available fiat currencies for this market
    __FIAT_CURRENCIES = [
        Currency('USD'),
        Currency('EUR'),
        Currency('JPY'),
        Currency('CAD'),
        Currency('GBP'),
        Currency('CHF'),
        Currency('RUB'),
        Currency('AUD'),
        Currency('SEK'),
        Currency('DKK'),
        Currency('HKD'),
        Currency('PLN'),
        Currency('CNY'),
        Currency('SGD'),
        Currency('THB'),
        Currency('NZD'),
        Currency('NOK'),
        Currency('CZK'),
        ]

    # how currencies have to be shifted in terms of decimal places
    # between the market and the internal representation
    __SHIFT = {
        'BTC': 0,
        'JPY': 5,
        'SEK': 5,
        }

    # constants to select order type
    # when querying order book data
    ORDER_TYPE_BID = 0
    ORDER_TYPE_ASK = 1

    signal_log = pyqtSignal(str)
    signal_wallet = pyqtSignal()
    signal_orderlag = pyqtSignal('long long', str)
    signal_userorder = pyqtSignal(object, object, str, str, str)
    signal_orderbook_changed = pyqtSignal()

    def __init__(self, preferences):
        QObject.__init__(self)
        self.__key = ''
        self.__secret = ''
        self.__preferences = preferences
        self.__preferences.set_fiat_currencies(Market.__FIAT_CURRENCIES)

    def __create_gox(self):

        # these settings are currently recommended by prof7bit
        goxapi.FORCE_PROTOCOL = 'websocket'
        goxapi.FORCE_HTTP_API = 'True'

        # initialize config from our preferences
        config = goxapi.GoxConfig("goxtool.ini")
        config.set('gox', 'quote_currency',
            self.__preferences.get_currency(
                Preferences.CURRENCY_INDEX_QUOTE).symbol)
        config.save()

        # initialize secret from our preferences
        secret = goxapi.Secret(config)
        secret.key = self.__preferences.get_key()
        secret.secret = self.__preferences.get_secret()
        gox = goxapi.Gox(secret, config)

        # connect to gox' signals
        gox.signal_debug.connect(self.__slot_log)
        gox.signal_wallet.connect(self.__slot_wallet_changed)
        gox.signal_orderlag.connect(self.__slot_orderlag)
        gox.signal_userorder.connect(self.__slot_userorder)
        gox.signal_fulldepth.connect(self.__slot_fulldepth)
        gox.signal_depth.connect(self.__slot_depth)

        return gox

    # start private methods

    def __get_currency_shift(self, index):
        '''
        Retrieves the difference in decimal places between the
        external representation (i.e. market) and the
        internal representation (i.e. application).
        '''
        symbol = self.__preferences.get_currency(index).symbol

        if symbol in Market.__SHIFT:
            return Market.__SHIFT[symbol]

        # the default shift is 3
        return 3

    def __to_internal(self, index, value):
        '''
        Converts an external money value (integer value) into
        an internal money value (a money object).
        '''
        return Money(value * pow(10, self.__get_currency_shift(index)),
            self.__preferences.get_currency(index), False)

    def __to_external(self, index, money):
        '''
        Converts an internal money value (a money object) into
        an external money value (integer)
        '''
        return money.value / pow(10, self.__get_currency_shift(index))

    def __slot_log(self, dummy, (text)):
        self.signal_log.emit(text)

    def __slot_fulldepth(self, dummy, data):
        self.signal_orderbook_changed.emit()

    def __slot_depth(self, dummy, data):
        self.signal_orderbook_changed.emit()

    def __slot_orderlag(self, dummy, (ms, text)):
        self.signal_orderlag.emit(ms, text)

    def __slot_wallet_changed(self, dummy, (text)):
        self.signal_wallet.emit()

    def __slot_userorder(self, dummy, data):

        (price, size, order_type, oid, status_message) = data

        price = self.__to_internal(Preferences.CURRENCY_INDEX_QUOTE, price)
        size = self.__to_internal(Preferences.CURRENCY_INDEX_BASE, size)

        self.signal_userorder.emit(
            price, size, order_type, oid, status_message)

    # start public methods

    def start(self):
        '''
        Activates the market
        '''
        self.gox = self.__create_gox()
        self.gox.start()

    def stop(self):
        '''
        Deactivates the market
        '''
        self.gox.stop()
        del self.gox
        time.sleep(1)

    def buy(self, price, size):
        '''
        Places buy order
        '''
        price = self.__to_external(Preferences.CURRENCY_INDEX_QUOTE, price)
        size = self.__to_external(Preferences.CURRENCY_INDEX_BASE, size)
        self.gox.buy(price, size)

    def sell(self, price, size):
        '''
        Places sell order
        '''
        price = self.__to_external(Preferences.CURRENCY_INDEX_QUOTE, price)
        size = self.__to_external(Preferences.CURRENCY_INDEX_BASE, size)
        self.gox.sell(price, size)

    def cancel(self, order_id):
        '''
        Cancels order
        '''
        self.gox.cancel(order_id)

    def get_balance(self, index):
        '''
        Returns the account balance for the currency with the specified index.
        @param index: base or quote
        @return: the balance or None if no balance available for this currency
        '''
        symbol = self.__preferences.get_currency(index).symbol
        if not symbol in self.gox.wallet:
            return None

        return self.__to_internal(index, self.gox.wallet[symbol])

    def get_order(self, typ, index):
        '''
        Retrieves the order of the specified type with the specified index.
        @param typ: ask or bid
        @param index: the row index
        '''
        if typ == Market.ORDER_TYPE_ASK:
            data = self.gox.orderbook.asks[index]
        elif typ == Market.ORDER_TYPE_BID:
            data = self.gox.orderbook.bids[index]
        else:
            raise Exception('invalid order type {}'.format(typ))

        price = self.__to_internal(
            Preferences.CURRENCY_INDEX_QUOTE,
            int(data.price))

        volume = self.__to_internal(
            Preferences.CURRENCY_INDEX_BASE,
            int(data.volume))

        return [price, volume]

    def get_order_count(self, typ):
        '''
        Retrieves the amount of orders available of the specified type.
        @param typ: ask or bid
        '''
        if not hasattr(self, 'gox'):
            return 0

        if typ == Market.ORDER_TYPE_ASK:
            return len(self.gox.orderbook.asks)

        if typ == Market.ORDER_TYPE_BID:
            return len(self.gox.orderbook.bids)

        raise Exception('invalid order type {}'.format(typ))

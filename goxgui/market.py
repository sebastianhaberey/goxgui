from PyQt4.QtCore import QObject, pyqtSignal
from currency import Currency
from preferences import Preferences
import goxapi
import time


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

    # these constants mark the type of orders, trades etc
    TYPE_BID = 0
    TYPE_ASK = 1

    # we're using objects as paramters for the signals,
    # because long integers will cause type errors
    # (with both type long and type 'long long')

    # log message
    signal_log = pyqtSignal(str)

    # none
    signal_wallet = pyqtSignal()

    # milliseconds
    signal_orderlag = pyqtSignal(object, str)

    # price, size, order type, order id, status
    signal_userorder = pyqtSignal(object, object, str, str, str)

    # price, size
    signal_bid = pyqtSignal(object, object)

    # list of [price, size]
    signal_bids = pyqtSignal(object)

    # price, size
    signal_ask = pyqtSignal(object, object)

    # list of [price, size]
    signal_asks = pyqtSignal(object)

    # bid, ask
    signal_ticker = pyqtSignal(object, object)

    # price, size, type
    signal_trade = pyqtSignal(object, object, object)

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
        gox.orderbook.signal_fulldepth_processed.connect(self.__slot_fulldepth)
        gox.signal_depth.connect(self.__slot_depth)
        gox.signal_ticker.connect(self.__slot_ticker)
        gox.signal_trade.connect(self.__slot_trade)

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
        Converts an external money value into an internal money value.
        '''
        return long(value) * pow(10, self.__get_currency_shift(index))

    def __to_external(self, index, value):
        '''
        Converts an internal money value into an external money value.
        '''
        return value / pow(10, self.__get_currency_shift(index))

    def __slot_log(self, dummy, (text)):
        self.signal_log.emit(text)

    def __slot_fulldepth(self, dummy, data):
        self.signal_bids.emit(self.__convert_orders(self.gox.orderbook.bids))
        self.signal_asks.emit(self.__convert_orders(self.gox.orderbook.asks))

    def __convert_orders(self, data):

        out = []
        for i in data:
            price = self.__to_internal(
                Preferences.CURRENCY_INDEX_QUOTE, i.price)
            volume = self.__to_internal(
                Preferences.CURRENCY_INDEX_BASE, i.volume)
            out.append([price, volume])
        return out

    def __slot_ticker(self, dummy, data):
        (bid, ask) = data
        bid = self.__to_internal(
            Preferences.CURRENCY_INDEX_QUOTE, bid)
        ask = self.__to_internal(
            Preferences.CURRENCY_INDEX_QUOTE, ask)
        self.signal_ticker.emit(bid, ask)

    def __slot_trade(self, dummy, data):
        (dummy_date, price, size, typ, own) = data
        if (own):
            return

        price = self.__to_internal(Preferences.CURRENCY_INDEX_QUOTE, price)
        size = self.__to_internal(Preferences.CURRENCY_INDEX_BASE, size)

        if typ == 'bid':
            typ = Market.TYPE_BID
        if typ == 'ask':
            typ = Market.TYPE_ASK

        self.signal_trade.emit(price, size, typ)

    def __slot_depth(self, dummy, data):

        (typ, price, _voldiff, total_vol) = data

        price = self.__to_internal(
            Preferences.CURRENCY_INDEX_QUOTE, price)
        total_vol = self.__to_internal(
            Preferences.CURRENCY_INDEX_BASE, total_vol)

        if typ == "ask":
            self.signal_ask.emit(price, total_vol)
        if typ == "bid":
            self.signal_bid.emit(price, total_vol)

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

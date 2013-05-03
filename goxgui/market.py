from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal
import goxapi
import utilities
import time


class Market(QObject):
    '''
    Wrapper for gox object used to decouple gui code
    from market implementation.
    '''

    signal_log = pyqtSignal(str)
    signal_wallet = pyqtSignal()
    signal_orderlag = pyqtSignal('long long', str)
    signal_userorder = pyqtSignal('long long', 'long long', str, str, str)
    signal_orderbook_changed = pyqtSignal(object)

    def __init__(self, preferences):
        QObject.__init__(self)
        self.__key = ''
        self.__secret = ''
        self.__preferences = preferences

    def __create_gox(self):

        goxapi.FORCE_PROTOCOL = 'websocket'
        goxapi.FORCE_HTTP_API = 'True'

        config = goxapi.GoxConfig("goxtool.ini")
        secret = goxapi.Secret(config)
        secret.key = self.__preferences.get_key()
        secret.secret = self.__preferences.get_secret()
        gox = goxapi.Gox(secret, config)

        gox.signal_debug.connect(self.slot_log)
        gox.signal_wallet.connect(self.slot_wallet_changed)
        gox.signal_orderlag.connect(self.slot_orderlag)
        gox.signal_userorder.connect(self.slot_userorder)
        gox.orderbook.signal_changed.connect(self.slot_orderbook_changed)

        return gox

    # start slots

    def slot_log(self, dummy_gox, (text)):
        self.signal_log.emit(text)

    def slot_orderbook_changed(self, orderbook, dummy):
        self.signal_orderbook_changed.emit(orderbook)

    def slot_orderlag(self, dummy_sender, (ms, text)):
        self.signal_orderlag.emit(ms, text)

    def slot_wallet_changed(self, dummy_gox, (text)):
        self.signal_wallet.emit()

    def slot_userorder(self, dummy_sender, data):
        (price, size, order_type, oid, status_message) = data
        self.signal_userorder.emit(
            price, size, order_type, oid, status_message)

    # end slots

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
        sizeGox = utilities.internal2gox(size, 'BTC')
        priceGox = utilities.internal2gox(price, 'USD')
        self.gox.buy(priceGox, sizeGox)

    def sell(self, price, size):
        '''
        Places sell order
        '''
        sizeGox = utilities.internal2gox(size, 'BTC')
        priceGox = utilities.internal2gox(price, 'USD')
        self.gox.sell(priceGox, sizeGox)

    def cancel(self, order_id):
        '''
        Cancels order
        '''
        self.gox.cancel(order_id)

    def get_balance(self, currency):
        '''
        Returns the account balance for the specified currency
        '''
        return self.gox.wallet[currency]

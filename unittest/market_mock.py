from PyQt4.QtCore import pyqtSignal, QObject
from money import to_money


class MarketMock(QObject):
    '''
    Mock object to simulate a market object in unit tests.
    Also used for profiling.
    '''

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

    def __init__(self):
        QObject.__init__(self)

    def depth_bid(self, price, volume):
        self.signal_bid.emit(to_money(price), to_money(volume))

    def depth_ask(self, price, volume):
        self.signal_ask.emit(to_money(price), to_money(volume))

    def depth_asks(self, depths):
        for depth in depths:
            depth[0] = to_money(depth[0])
            depth[1] = to_money(depth[1])
        self.signal_asks.emit(depths)

    def ticker(self, bid, ask):
        self.signal_ticker.emit(to_money(bid), to_money(ask))

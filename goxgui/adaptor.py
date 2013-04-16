from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal


class Adaptor(QObject):
    '''
    Adaptor that converts gox object signals to qt signals.
    '''

    signal_log = pyqtSignal(str)
    signal_wallet = pyqtSignal()
    signal_orderlag = pyqtSignal('long long', str)
    signal_userorder = pyqtSignal('long long', 'long long', str, str, str)

    def __init__(self, gox):
        QObject.__init__(self)
        self.gox = gox
        self.gox.signal_debug.connect(self.log)
        self.gox.signal_wallet.connect(self.wallet)
        self.gox.signal_orderlag.connect(self.orderlag)
        self.gox.signal_userorder.connect(self.userorder)

    def log(self, dummy_gox, (text)):
        self.signal_log.emit(text)

    def wallet(self, dummy_gox, (text)):
        self.signal_wallet.emit()

    def orderlag(self, dummy_sender, (ms, text)):
        self.signal_orderlag.emit(ms, text)

    def userorder(self, dummy_sender, data):
        (price, size, order_type, oid, status_message) = data
        self.signal_userorder.emit(
            price, size, order_type, oid, status_message)

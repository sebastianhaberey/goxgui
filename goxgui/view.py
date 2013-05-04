import utilities
import time
import logging

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTextCursor
from ui.main_window_ import Ui_MainWindow
from model import ModelAsk
from model import ModelBid


class View(QMainWindow):
    '''
    Represents the combined view / control.
    '''

    # how the application-proposed bid will differ from the selected bid
    ADD_TO_BID = 1000

    # how the application-proposed ask will differ from the selected ask
    SUB_FROM_ASK = 1000

    def __init__(self, preferences, market):

        QMainWindow.__init__(self)

        self.preferences = preferences
        self.market = market

        # set up main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect market signals to our logic
        self.market.signal_log.connect(self.slot_log)
        self.market.signal_wallet.connect(self.display_wallet)
        self.market.signal_orderlag.connect(self.display_orderlag)
        self.market.signal_userorder.connect(self.display_userorder)

        # connect ui signals to our logic
        self.ui.pushButtonGo.released.connect(
            self.execute_trade)
        self.ui.tableAsk.clicked.connect(
            self.update_price_from_asks)
        self.ui.tableBid.clicked.connect(
            self.update_price_from_bids)
        self.ui.pushButtonCancel.released.connect(
            self.cancel_order)
        self.ui.textBrowserStatus.anchorClicked.connect(
            self.order_selected)
        self.ui.pushButtonWalletA.released.connect(
            self.set_trade_size_from_wallet)
        self.ui.pushButtonWalletB.released.connect(
            self.set_trade_total_from_wallet)
        self.ui.pushButtonSize.released.connect(
            self.recalculate_size)
        self.ui.pushButtonPrice.released.connect(
            self.update_price_best)
        self.ui.pushButtonTotal.released.connect(
            self.recalculate_total)
        self.ui.actionPreferences_2.triggered.connect(
            self.show_preferences)

        # initialize and connect bid / ask table models
        self.modelAsk = ModelAsk(self.market)
        self.ui.tableAsk.setModel(self.modelAsk)
        self.modelBid = ModelBid(self.market)
        self.ui.tableBid.setModel(self.modelBid)

        # associate log channels with their check boxes
        self.logchannels = [
            [self.ui.checkBoxLogTicker, 'tick'],
            [self.ui.checkBoxLogTrade, 'TRADE'],
            [self.ui.checkBoxLogDepth, 'depth'],
        ]

        # activate market
        self.market.start()

        # show main window
        self.adjustSize()
        self.show()
        self.raise_()

    def show_preferences(self):

        result = self.preferences.show()
        if result == True:
            self.status_message('Preferences changed, restarting market.')
            self.market.stop()
            self.preferences.apply()
            self.market.start()
            self.status_message('Market restarted successfully.')

    def get_selected_trade_type(self):
        if self.ui.radioButtonBuy.isChecked():
            return 'BUY'
        else:
            return 'SELL'

    def set_selected_trade_type(self, trade_type):
        if trade_type == 'BUY':
            self.ui.radioButtonBuy.toggle()
        else:
            self.ui.radioButtonSell.toggle()

    def slot_log(self, text):

        logging.info(text)
        text = self.prepend_date(text)

        doOutput = False

        if self.ui.checkBoxLogSystem.isChecked():
            doOutput = True

        for entry in self.logchannels:
            if entry[1] in text:
                doOutput = entry[0].isChecked()

        if doOutput:
            self.ui.textBrowserLog.append(text)

    def prepend_date(self, text):
        millis = int(round(time.time() * 1000)) % 1000
        return '{}.{:0>3} {}'.format(time.strftime('%X'), millis, text)

    def status_message(self, text):
        # call move cursor before append to work around link clicking bug
        # see: https://bugreports.qt-project.org/browse/QTBUG-539
        logging.info(text)
        text = self.prepend_date(text)
        self.ui.textBrowserStatus.moveCursor(QTextCursor.End)
        self.ui.textBrowserStatus.append(text)

    def set_wallet_btc(self, value):
        self.ui.pushButtonWalletA.setEnabled(value > 0)
        self.ui.pushButtonWalletA.setText(
            'BTC: ' + utilities.internal2str(value))

    def set_wallet_usd(self, value):
        self.ui.pushButtonWalletB.setEnabled(value > 0)
        self.ui.pushButtonWalletB.setText(
            'USD: ' + utilities.internal2str(value, 5))

    def get_trade_size(self):
        value = self.ui.doubleSpinBoxBtc.value()
        return utilities.float2internal(value)

    def set_trade_size(self, value):
        value_float = utilities.internal2float(value)
        self.ui.doubleSpinBoxBtc.setValue(value_float)

    def get_trade_price(self):
        value = self.ui.doubleSpinBoxPrice.value()
        return utilities.float2internal(value)

    def set_trade_price(self, value):
        value_float = utilities.internal2float(value)
        self.ui.doubleSpinBoxPrice.setValue(value_float)

    def get_trade_total(self):
        value = self.ui.doubleSpinBoxTotal.value()
        return utilities.float2internal(value)

    def set_trade_total(self, value):
        value_float = utilities.internal2float(value)
        self.ui.doubleSpinBoxTotal.setValue(value_float)

    def get_order_id(self):
        return str(self.ui.lineEditOrder.text())

    def set_order_id(self, text):
        self.ui.lineEditOrder.setText(text)

    def order_selected(self, url):
        self.set_order_id(str(url.toString()))

    def display_wallet(self):

        self.set_wallet_usd(
            utilities.gox2internal(self.market.get_balance('USD'), 'USD'))
        self.set_wallet_btc(
            utilities.gox2internal(self.market.get_balance('BTC'), 'BTC'))

    def set_trade_size_from_wallet(self):
        self.set_trade_size(
            utilities.gox2internal(self.market.get_balance('BTC'), 'BTC'))
        self.set_selected_trade_type('SELL')

    def set_trade_total_from_wallet(self):
        self.set_trade_total(
            utilities.gox2internal(self.market.get_balance('USD'), 'USD'))
        self.set_selected_trade_type('BUY')

    def display_orderlag(self, ms, text):
        self.ui.labelOrderlag.setText('Trading Lag: ' + text)

    def execute_trade(self):

        trade_type = self.get_selected_trade_type()

        size = self.get_trade_size()
        price = self.get_trade_price()
        total = self.get_trade_total()

        trade_name = 'BID' if trade_type == 'BUY' else 'ASK'

        self.status_message('Placing order: {0} {1} BTC at {2} USD (total {3} USD)...'.format(# @IgnorePep8
            trade_name,
            utilities.internal2str(size),
            utilities.internal2str(price, 5),
            utilities.internal2str(total, 5)))

        if trade_type == 'BUY':
            self.market.buy(price, size)
        else:
            self.market.sell(price, size)

    def recalculate_size(self):

        price = self.get_trade_price()
        if price == 0:
            return

        total = self.get_trade_total()
        size = utilities.divide_internal(total, price)
        self.set_trade_size(size)

    def recalculate_total(self):

        price = self.get_trade_price()
        size = self.get_trade_size()
        total = utilities.multiply_internal(price, size)
        self.set_trade_total(total)

    def display_userorder(self, price, size, order_type, oid, status):

        size = utilities.gox2internal(size, 'BTC')
        price = utilities.gox2internal(price, 'USD')

        size = utilities.internal2str(size)
        price = utilities.internal2str(price)

        if order_type == '':
            self.status_message("Order <a href=\"{0}\">{0}</a> {1}.".format(
                oid, status))
            if status == 'removed' and self.get_order_id() == oid:
                self.set_order_id('')
        else:
            self.status_message("{0} size: {1}, price: {2}, oid: <a href=\"{3}\">{3}</a> - {4}".format(# @IgnorePep8
                str.upper(str(order_type)), size, price, oid, status))
            if status == 'post-pending':
                self.set_order_id(oid)

    def update_price_from_asks(self, index):
        self.set_trade_price(self.modelAsk.get_price(index.row())
            - self.SUB_FROM_ASK)

    def update_price_from_bids(self, index):
        self.set_trade_price(self.modelBid.get_price(index.row())
            + self.ADD_TO_BID)

    def cancel_order(self):
        order_id = self.get_order_id()
        self.status_message(
            "Cancelling order <a href=\"{0}\">{0}</a>...".format(order_id))
        self.market.cancel(order_id)

    def update_price_best(self):

        trade_type = self.get_selected_trade_type()
        if trade_type == 'BUY':
            price = self.modelBid.get_price(0)
            price += self.ADD_TO_BID
            self.set_trade_price(price)
        elif trade_type == 'SELL':
            price = self.modelAsk.get_price(0)
            price -= self.SUB_FROM_ASK
            self.set_trade_price(price)

    def stop(self):
        self.market.stop()

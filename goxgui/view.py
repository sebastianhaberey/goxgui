import utilities
import time
import logging

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTextCursor
from ui.main_window_ import Ui_MainWindow
from model import ModelAsk
from model import ModelBid
from PyQt4 import QtGui
from money import Money
from preferences import Preferences


class View(QMainWindow):
    '''
    Represents the combined view / control.
    '''

    # how the application-proposed bid
    # will differ from the selected bid (in pips)
    ADD_TO_BID_PIPS = 1

    # how the application-proposed ask
    # will differ from the selected ask (in pips)
    SUB_FROM_ASK_PIPS = 1

    def __init__(self, preferences, market):

        QMainWindow.__init__(self)

        self.preferences = preferences
        self.market = market

        # set up main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # improve ui on mac
        if utilities.platform_is_mac():
            self.adjust_for_mac()

        # connect market signals to our logic
        self.market.signal_log.connect(self.slot_log)
        self.market.signal_wallet.connect(self.display_wallet)
        self.market.signal_orderlag.connect(self.display_orderlag)
        self.market.signal_userorder.connect(self.display_userorder)

        # connect ui signals to our logic
        self.ui.pushButtonGo.released.connect(
            self.execute_trade)
        self.ui.tableAsk.clicked.connect(
            self.slot_update_price_from_asks)
        self.ui.tableBid.clicked.connect(
            self.slot_update_price_from_bids)
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
        self.modelAsk = ModelAsk(self, self.market, preferences)
        self.ui.tableAsk.setModel(self.modelAsk)
        self.modelBid = ModelBid(self, self.market, preferences)
        self.ui.tableBid.setModel(self.modelBid)

        # associate log channels with their check boxes
        self.logchannels = [
            [self.ui.checkBoxLogTicker, 'tick'],
            [self.ui.checkBoxLogTrade, 'TRADE'],
            [self.ui.checkBoxLogDepth, 'depth'],
        ]

        # resets dynamic ui elements
        self.reset()

        # activate market
        self.market.start()

        # show main window
        self.adjustSize()
        self.show()
        self.raise_()

    def reset(self):

        # initialize wallet values
        self.set_wallet_a(None)
        self.set_wallet_b(None)

        # adjust decimal values to current currencies
        self.adjust_decimals()

    def adjust_decimals(self):
        currencyQuote = self.preferences.get_currency(
            Preferences.CURRENCY_INDEX_QUOTE)
        currencyBase = self.preferences.get_currency(
            Preferences.CURRENCY_INDEX_BASE)
        self.ui.doubleSpinBoxSize.setDecimals(currencyBase.decimals)
        self.ui.doubleSpinBoxPrice.setDecimals(currencyQuote.decimals)
        self.ui.doubleSpinBoxTotal.setDecimals(currencyQuote.decimals)

    def adjust_for_mac(self):
        '''
        Fixes some stuff that looks good on windows but bad on mac.
        '''
        # the default fixed font is unreadable on mac, so replace it
        font = QtGui.QFont('Monaco', 11)
        self.ui.tableAsk.setFont(font)
        self.ui.tableBid.setFont(font)
        self.ui.textBrowserLog.setFont(font)
        self.ui.textBrowserStatus.setFont(font)
        self.ui.lineEditOrder.setFont(font)
        self.ui.doubleSpinBoxSize.setFont(font)
        self.ui.doubleSpinBoxPrice.setFont(font)
        self.ui.doubleSpinBoxTotal.setFont(font)

        # the space between application title bar and
        # the ui elements is too small on mac
        margins = self.ui.widgetMain.layout().contentsMargins()
        margins.setTop(24)
        self.ui.widgetMain.layout().setContentsMargins(margins)

    def show_preferences(self):

        result = self.preferences.show()
        if result == True:
            self.status_message('Preferences changed, restarting market.')
            self.market.stop()
            self.preferences.apply()
            self.reset()
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

    def set_wallet_a(self, value):

        if value == None:
            self.ui.pushButtonWalletA.setEnabled(False)
            self.ui.pushButtonWalletA.setText('n/a')
            return

        self.ui.pushButtonWalletA.setEnabled(True)
        self.ui.pushButtonWalletA.setText(value.to_long_string())

    def set_wallet_b(self, value):

        if value == None:
            self.ui.pushButtonWalletB.setEnabled(False)
            self.ui.pushButtonWalletB.setText('n/a')
            return

        self.ui.pushButtonWalletB.setEnabled(True)
        self.ui.pushButtonWalletB.setText(value.to_long_string())

    def get_trade_size(self):
        # re-convert trade size float value from gui
        # to proper base currency value
        return Money(self.ui.doubleSpinBoxSize.value(),
            self.preferences.get_currency(Preferences.CURRENCY_INDEX_BASE))

    def set_trade_size(self, value):
        self.ui.doubleSpinBoxSize.setValue(value.to_float())

    def get_trade_price(self):
        # re-convert trade price value from gui
        # to proper quote currency value
        return Money(self.ui.doubleSpinBoxPrice.value(),
            self.preferences.get_currency(Preferences.CURRENCY_INDEX_QUOTE))

    def set_trade_price(self, value):
        self.ui.doubleSpinBoxPrice.setValue(value.to_float())

    def get_trade_total(self):
        # re-convert trade total value from gui
        # to proper quote currency value
        return Money(self.ui.doubleSpinBoxTotal.value(),
            self.preferences.get_currency(Preferences.CURRENCY_INDEX_QUOTE))

    def set_trade_total(self, value):
        self.ui.doubleSpinBoxTotal.setValue(value.to_float())

    def get_order_id(self):
        return str(self.ui.lineEditOrder.text())

    def set_order_id(self, text):
        self.ui.lineEditOrder.setText(text)

    def order_selected(self, url):
        self.set_order_id(str(url.toString()))

    def display_wallet(self):

        self.set_wallet_a(self.market.get_balance(
            Preferences.CURRENCY_INDEX_BASE))
        self.set_wallet_b(self.market.get_balance(
            Preferences.CURRENCY_INDEX_QUOTE))

    def set_trade_size_from_wallet(self):
        self.set_trade_size(
            self.market.get_balance(Preferences.CURRENCY_INDEX_BASE))
        self.set_selected_trade_type('SELL')

    def set_trade_total_from_wallet(self):
        self.set_trade_total(
            self.market.get_balance(Preferences.CURRENCY_INDEX_QUOTE))
        self.set_selected_trade_type('BUY')

    def display_orderlag(self, ms, text):
        self.ui.labelOrderlag.setText('Trading Lag: ' + text)

    def execute_trade(self):

        trade_type = self.get_selected_trade_type()

        size = self.get_trade_size()
        price = self.get_trade_price()
        total = price * size

        trade_name = 'BID' if trade_type == 'BUY' else 'ASK'

        self.status_message('Placing order: {0} {1} at {2} (total {3})...'.format(# @IgnorePep8
            trade_name,
            size.to_long_string(),
            price.to_long_string(),
            total.to_long_string()))

        if trade_type == 'BUY':
            self.market.buy(price, size)
        else:
            self.market.sell(price, size)

    def recalculate_size(self):

        price = self.get_trade_price()

        if price.value == 0:
            return

        total = self.get_trade_total()
        size = total / price

        # we multiply quote currency values but the resulting
        # size must be expressed in base currency
        size.currency = self.preferences.get_currency(
            Preferences.CURRENCY_INDEX_BASE)

        self.set_trade_size(size)

    def recalculate_total(self):

        price = self.get_trade_price()
        size = self.get_trade_size()
        total = price * size

        # ToDo: set currency type
        self.set_trade_total(total)

    def display_userorder(self, price, size, order_type, oid, status):

        if order_type == '':
            self.status_message("Order <a href=\"{0}\">{0}</a> {1}.".format(
                oid, status))
            if status == 'removed' and self.get_order_id() == oid:
                self.set_order_id('')
        else:
            self.status_message("{0} size: {1}, price: {2}, oid: <a href=\"{3}\">{3}</a> - {4}".format(# @IgnorePep8
                str.upper(str(order_type)),
                size.to_long_string(),
                price.to_long_string(),
                oid,
                status))
            if status == 'post-pending':
                self.set_order_id(oid)

    def slot_update_price_from_asks(self, index):
        self.update_price_from_asks(index.row())

    def update_price_from_asks(self, row):
        value = self.modelAsk.get_price(row)
        pip = value.pip() * Money(View.SUB_FROM_ASK_PIPS)
        self.set_trade_price(value - pip)

    def slot_update_price_from_bids(self, index):
        self.update_price_from_bids(index.row())

    def update_price_from_bids(self, row):
        value = self.modelBid.get_price(row)
        pip = value.pip() * Money(View.ADD_TO_BID_PIPS)
        self.set_trade_price(value + pip)

    def cancel_order(self):
        order_id = self.get_order_id()
        self.status_message(
            "Cancelling order <a href=\"{0}\">{0}</a>...".format(order_id))
        self.market.cancel(order_id)

    def update_price_best(self):

        trade_type = self.get_selected_trade_type()
        if trade_type == 'BUY':
            self.update_price_from_bids(0)
        elif trade_type == 'SELL':
            self.update_price_from_asks(0)

    def stop(self):
        self.market.stop()

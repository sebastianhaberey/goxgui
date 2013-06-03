import utilities
import time
import logging
import money

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QHeaderView
from ui.main_window_ import Ui_MainWindow
from model import Model
from orders import Orders
from PyQt4 import QtGui
from preferences import Preferences
from market import Market
from info import Info


class View(QMainWindow):
    '''
    Represents the combined view / control.
    '''

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
        self.market.signal_ticker.connect(self.update_ticker)

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
        self.ui.pushButtonSize.released.connect(
            self.recalculate_size)
        self.ui.pushButtonPrice.released.connect(
            self.update_price_best)
        self.ui.pushButtonTotal.released.connect(
            self.recalculate_total)
        self.ui.actionPreferences_2.triggered.connect(
            self.show_preferences)

        # associate log channels with their check boxes
        self.logchannels = [
            [self.ui.checkBoxLogTicker, 'tick'],
            [self.ui.checkBoxLogTrade, 'TRADE'],
            [self.ui.checkBoxLogDepth, 'depth'],
        ]

        # set correct resizing for the bid and ask tables
        self.ui.tableAsk.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.ui.tableBid.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # set up info table
        self.info = Info(self, self.preferences, self.ui.tableInfo.clicked)
        self.ui.tableInfo.setModel(self.info)
        self.ui.tableInfo.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # connect to signals from info table
        self.info.signal_base_balance_clicked.connect(
            self.set_trade_size_from_wallet)
        self.info.signal_quote_balance_clicked.connect(
            self.set_trade_total_from_wallet)

        # initializes dynamic ui elements
        self.init()

        # activate market
        self.market.start()

        # show main window
        self.adjustSize()
        self.show()
        self.raise_()

    def get_base_currency(self):
        return self.preferences.get_currency(Preferences.CURRENCY_INDEX_BASE)

    def get_quote_currency(self):
        return self.preferences.get_currency(Preferences.CURRENCY_INDEX_QUOTE)

    def init(self):

        # initialize wallet values
        self.info.set_wallet_a(None)
        self.info.set_wallet_b(None)

        # initialize ticker values
        self.info.set_ticker_ask(None)
        self.info.set_ticker_bid(None)

        # adjust decimal values to current currencies
        self.adjust_decimals()

        # set up table models
        self.init_models()

    def init_models(self):

        self.orders_ask = Orders(self.market, Market.TYPE_ASK,
            self.preferences.get_grouping())
        self.model_ask = Model(self, self.orders_ask, self.preferences)
        self.ui.tableAsk.setModel(self.model_ask)

        self.orders_bid = Orders(self.market, Market.TYPE_BID,
            self.preferences.get_grouping())
        self.model_bid = Model(self, self.orders_bid, self.preferences)
        self.ui.tableBid.setModel(self.model_bid)

    def adjust_decimals(self):
        currencyQuote = self.get_quote_currency()
        currencyBase = self.get_base_currency()
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
        self.ui.tableInfo.setFont(font)
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
            self.init()
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

    def get_trade_size(self):
        return money.to_money(self.ui.doubleSpinBoxSize.value())

    def set_trade_size(self, value):
        self.ui.doubleSpinBoxSize.setValue(money.to_float(value))

    def get_trade_price(self):
        return money.to_money(self.ui.doubleSpinBoxPrice.value())

    def set_trade_price(self, value):
        self.ui.doubleSpinBoxPrice.setValue(money.to_float(value))

    def get_trade_total(self):
        return money.to_money(self.ui.doubleSpinBoxTotal.value())

    def set_trade_total(self, value):
        self.ui.doubleSpinBoxTotal.setValue(money.to_float(value))

    def get_order_id(self):
        return str(self.ui.lineEditOrder.text())

    def set_order_id(self, text):
        self.ui.lineEditOrder.setText(text)

    def order_selected(self, url):
        self.set_order_id(str(url.toString()))

    def display_wallet(self):

        self.info.set_wallet_a(self.market.get_balance(
            Preferences.CURRENCY_INDEX_BASE))
        self.info.set_wallet_b(self.market.get_balance(
            Preferences.CURRENCY_INDEX_QUOTE))

    def update_ticker(self, bid, ask):

        self.info.set_ticker_bid(bid)
        self.info.set_ticker_ask(ask)

    def set_trade_size_from_wallet(self):
        self.set_trade_size(
            self.market.get_balance(Preferences.CURRENCY_INDEX_BASE))
        self.set_selected_trade_type('SELL')

    def set_trade_total_from_wallet(self):
        self.set_trade_total(
            self.market.get_balance(Preferences.CURRENCY_INDEX_QUOTE))
        self.set_selected_trade_type('BUY')

    def display_orderlag(self, ms, text):
        self.info.set_orderlag(ms)

    def execute_trade(self):

        trade_type = self.get_selected_trade_type()

        size = self.get_trade_size()
        price = self.get_trade_price()
        total = money.multiply(price, size)

        trade_name = 'BID' if trade_type == 'BUY' else 'ASK'

        self.status_message('Placing order: {0} {1} at {2} (total {3})...'.format(# @IgnorePep8
            trade_name,
            money.to_long_string(size, self.get_base_currency()),
            money.to_long_string(price, self.get_quote_currency()),
            money.to_long_string(total, self.get_quote_currency())))

        if trade_type == 'BUY':
            self.market.buy(price, size)
        else:
            self.market.sell(price, size)

    def recalculate_size(self):

        price = self.get_trade_price()

        if price == 0:
            return

        total = self.get_trade_total()
        size = money.divide(total, price)
        self.set_trade_size(size)

    def recalculate_total(self):

        price = self.get_trade_price()
        size = self.get_trade_size()
        total = money.multiply(price, size)

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
                money.to_long_string(size, self.get_base_currency()),
                money.to_long_string(price, self.get_quote_currency()),
                oid,
                status))
            if status == 'post-pending':
                self.set_order_id(oid)

    def slot_update_price_from_asks(self, index):
        self.update_price_from_asks(index.row())

    def update_price_from_asks(self, row):
        value = self.orders_ask.get_price(row)
        pip = money.pip(
            self.get_quote_currency()) * self.preferences.get_proposed_pips()
        self.set_trade_price(value - pip)

    def slot_update_price_from_bids(self, index):
        self.update_price_from_bids(index.row())

    def update_price_from_bids(self, row):
        value = self.orders_bid.get_price(row)
        pip = money.pip(
            self.get_quote_currency()) * self.preferences.get_proposed_pips()
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

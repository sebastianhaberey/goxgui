from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt, SIGNAL, pyqtSignal
from PyQt4.QtGui import QColor
from preferences import Preferences
import money


class Info(QAbstractTableModel):
    '''
    Model that represents a table with various information.
    '''

    __ROWS = 2
    __COLS = 6

    __COLOR_DEFAULT = QColor(255, 255, 255)
    __COLOR_BID_ASK = QColor(240, 255, 240)
    __COLOR_BALANCE = QColor(240, 240, 255)
    __COLOR_ORDERLAG = QColor(237, 243, 254)

    signal_base_balance_clicked = pyqtSignal()
    signal_quote_balance_clicked = pyqtSignal()

    def __init__(self, parent, preferences, signal_clicked):
        QAbstractTableModel.__init__(self, parent)

        # initialize data array with empty strings
        self.__data = [['' for i in range(self.__COLS)] for j in range(self.__ROWS)]  # @UnusedVariable @IgnorePep8

        # initialize color array with default color
        self.__color = [[self.__COLOR_DEFAULT for i in range(self.__COLS)] for j in range(self.__ROWS)]  # @UnusedVariable @IgnorePep8

        self.__preferences = preferences

        # initialize non-changing cell texts and colors
        self.__set_data(0, 0, "Crypto balance:")
        self.__set_data(1, 0, "Fiat balance:")
#         self.__set_color(0, 0, self.__COLOR_BALANCE)
#         self.__set_color(0, 1, self.__COLOR_BALANCE)
#         self.__set_color(1, 0, self.__COLOR_BALANCE)
#         self.__set_color(1, 1, self.__COLOR_BALANCE)

        self.__set_data(0, 2, "Trading lag:")
        self.__set_color(0, 2, self.__COLOR_ORDERLAG)
        self.__set_color(0, 3, self.__COLOR_ORDERLAG)
        self.__set_color(1, 2, self.__COLOR_ORDERLAG)
        self.__set_color(1, 3, self.__COLOR_ORDERLAG)

        self.__set_data(0, 4, "Bid:")
        self.__set_data(1, 4, "Ask:")
#         self.__set_color(0, 4, self.__COLOR_BID_ASK)
#         self.__set_color(0, 5, self.__COLOR_BID_ASK)
#         self.__set_color(1, 4, self.__COLOR_BID_ASK)
#         self.__set_color(1, 5, self.__COLOR_BID_ASK)

        # listen for clicks
        signal_clicked.connect(self.__slot_clicked)

    # private methods

    def __set_data(self, row, col, text):
        self.__data[row][col] = text
        self.emit(SIGNAL("layoutChanged()"))

    def __set_color(self, row, col, color):
        self.__color[row][col] = color
        self.emit(SIGNAL("layoutChanged()"))

    def __slot_clicked(self, index):
        row = index.row()
        col = index.column()

        if row == 0 and (col == 0 or col == 1):
            self.signal_base_balance_clicked.emit()
            return

        if row == 1 and (col == 0 or col == 1):
            self.signal_quote_balance_clicked.emit()
            return

    def __get_base_currency(self):
        return self.__preferences.get_currency(
            Preferences.CURRENCY_INDEX_BASE)

    def __get_quote_currency(self):
        return self.__preferences.get_currency(
            Preferences.CURRENCY_INDEX_QUOTE)

    # Qt methods

    def rowCount(self, parent):
        return self.__ROWS

    def columnCount(self, parent):
        return self.__COLS

    def data(self, index, role):

        row = index.row()
        col = index.column()

        if role == Qt.TextAlignmentRole:
            if col % 2 == 0:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role == Qt.BackgroundRole:
            if col % 2 == 1:
                return self.__COLOR_DEFAULT
            else:
                return self.__COLOR_ORDERLAG

        if (not index.isValid()) or (role != Qt.DisplayRole):
            return QVariant()

        return QVariant(self.__data[row][col])

    # public methods

    def set_wallet_a(self, value):

        if value == None:
            text = 'n/a'
        else:
            text = money.to_long_string(value, self.__get_base_currency())

        self.__set_data(0, 1, text)

    def set_wallet_b(self, value):

        if value == None:
            text = 'n/a'
        else:
            text = money.to_long_string(value, self.__get_quote_currency())

        self.__set_data(1, 1, text)

    def set_ticker_bid(self, value):

        if value == None:
            text = 'n/a'
        else:
            text = money.to_long_string(value, self.__get_quote_currency())

        self.__set_data(0, 5, text)

    def set_ticker_ask(self, value):

        if value == None:
            text = 'n/a'
        else:
            text = money.to_long_string(value, self.__get_quote_currency())

        self.__set_data(1, 5, text)

    def set_orderlag(self, ms):
        self.__set_data(0, 3, '{:.3f} s'.format(float(ms) / 1000000))

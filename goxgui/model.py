from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt, SIGNAL
from preferences import Preferences
import money
import weakref


class Model(QAbstractTableModel):
    '''
    Adapter that makes orders accessible to Qt.
    '''

    def __init__(self, parent, orders, preferences):
        QAbstractTableModel.__init__(self, parent)

        # Stale order book objects have to be deleted, otherwise
        # they will still receive and process signals from the market
        # and slow down the application.
        # Because Qt doesn't release the model properly,
        # we use a weak reference here to keep control
        # over the deletion of the order book.
        self.__orders = weakref.proxy(orders)

        self.__base_currency = preferences.get_currency(
                    Preferences.CURRENCY_INDEX_BASE)

        self.__quote_currency = preferences.get_currency(
                    Preferences.CURRENCY_INDEX_QUOTE)

        (self.__headers, self.__getters) = self.__create_columns(preferences)

        self.__orders.signal_changed.connect(self.__slot_update)

    # private methods

    def __create_columns(self, preferences):
        '''
        Creates headers and getter methods for the column data
        based on the specified preferences.
        '''

        headers = []
        getters = []

        if preferences.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_PRICE):

            headers.append('Price {}'.format(
                self.__quote_currency.symbol))
            getters.append(lambda index:
                [self.__orders.get_price(index), self.__quote_currency])

        if preferences.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_SIZE):

            headers.append('Size {}'.format(
                self.__base_currency.symbol))
            getters.append(lambda index:
                [self.__orders.get_volume(index), self.__base_currency])

        if preferences.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_QUOTE):

            headers.append('Quote {}'.format(
                self.__quote_currency.symbol))
            getters.append(lambda index:
                [self.__orders.get_quote(index), self.__quote_currency])

        if preferences.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_TOTAL):

            headers.append('Total {}'.format(
                self.__base_currency.symbol))
            getters.append(lambda index:
                [self.__orders.get_total(index), self.__base_currency])

        if preferences.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_TOTAL_QUOTE):

            headers.append('Total Quote {}'.format(
                self.__quote_currency.symbol))
            getters.append(lambda index:
                [self.__orders.get_total_quote(index), self.__quote_currency])

        return headers, getters

    def __slot_update(self):
        self.emit(SIGNAL("layoutChanged()"))

    def __get_header(self):
        return self.__headers

    # Qt methods

    def rowCount(self, parent):
        return self.__orders.size()

    def columnCount(self, parent):
        return len(self.__get_header())

    def data(self, index, role):

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight | Qt.AlignVCenter

        if (not index.isValid()) or (role != Qt.DisplayRole):
            return QVariant()

        (value, currency) = self.__getters[index.column()](index.row())
        return QVariant(money.to_string(value, currency))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.__get_header()[col])
        return QVariant()

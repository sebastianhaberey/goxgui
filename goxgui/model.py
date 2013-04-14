from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import SIGNAL
import utilities
import abc


class Model(QAbstractTableModel):
    '''
    Model representing a collection of orders.
    '''

    def __init__(self, gox, headerdata):
        QAbstractTableModel.__init__(self)
        self.gox = gox
        self.gox.orderbook.signal_changed.connect(self.__slot_changed)
        self.__headerdata = headerdata
        self.__data = []

    def __slot_changed(self, book, dummy_data):
        self.__data = self.__parse_data(book)
        self.emit(SIGNAL("layoutChanged()"))

    def __parse_data(self, book):
        '''
        Parses the incoming data from gox,
        converts money values to our internal
        money format
        '''
        data_in = self._get_data_from_book(book)
        data_out = []

        total_sum = 0

        for x in data_in:

            price = utilities.gox2internal(x.price, 'USD')
            size = utilities.gox2internal(x.volume, 'BTC')
            total = utilities.multiply_internal(price, size)
            total_sum += total

            data_out.append([price, size, total, total_sum])

        return data_out

    @abc.abstractmethod
    def _get_data_from_book(self, book):
        '''
        This method retrieves the orders relevant to this
        specific model from the order book.
        '''
        return []

    def get_price(self, index):
        return self.__data[index][0]

    def get_size(self, index):
        return self.__data[index][1]

    def get_total(self, index):
        return self.__data[index][2]

    def get_sum_total(self, index):
        return self.__data[index][3]

    # START Qt methods

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        return len(self.__headerdata)

    def data(self, index, role):

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight | Qt.AlignVCenter

        if (not index.isValid()) or (role != Qt.DisplayRole):
            return QVariant()

        row = index.row()
        col = index.column()

        if col == 0:
            return QVariant(utilities.internal2str(self.get_price(row)))
        if col == 1:
            return QVariant(utilities.internal2str(self.get_size(row)))
        if col == 2:
            return QVariant(utilities.internal2str(self.get_total(row), 5))
        if col == 3:
            return QVariant(utilities.internal2str(self.get_sum_total(row), 5))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.__headerdata[col])
        return QVariant()

    # END Qt methods


class ModelAsk(Model):

    def __init__(self, gox):
        Model.__init__(self, gox, ['Ask', 'Size', 'Total', 'Sum Total'])

    def _get_data_from_book(self, book):
        return book.asks


class ModelBid(Model):

    def __init__(self, gox):
        Model.__init__(self, gox, ['Bid', 'Size', 'Total', 'Sum Total'])

    def _get_data_from_book(self, book):
        return book.bids

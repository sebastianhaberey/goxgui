from PyQt4.QtCore import QObject, pyqtSignal
from level import Level
from market import Market
import money


class Orders(QObject):
    '''
    Represents a collection of ask or bid orders, grouped by levels.
    '''

    signal_changed = pyqtSignal()

    def __init__(self, market, typ, grouping=0):
        QObject.__init__(self)

        self.__typ = typ

        self.__market = market
        self.__market.signal_trade.connect(self.__slot_trade)
        self.__market.signal_ticker.connect(self.__slot_ticker)

        if typ == Market.TYPE_BID:

            self.__market.signal_bid.connect(self.__slot_depth)
            self.__market.signal_bids.connect(self.__slot_depths)
            self.__compare = lambda x, y: x > y

        elif typ == Market.TYPE_ASK:

            self.__market.signal_ask.connect(self.__slot_depth)
            self.__market.signal_asks.connect(self.__slot_depths)
            self.__compare = lambda x, y: x < y

        else:
            raise Exception('Invalid order book type {}.'.format(typ))

        self.__levels = []

        if grouping == 0:
            self.__grouping = 1
        else:
            self.__grouping = money.to_money(grouping)

    # private methods

    def __slot_trade(self, price, volume, typ):

        # if the trade is an ask it only affects the bids,
        # and if it is a bid it only affects the asks
        if (typ == self.__typ):
            return

        self.__delete_all(price)
        index = self.__subtract(price, volume)
        self.__recalculate_totals(index)
        self.signal_changed.emit()

    def __slot_depths(self, depths):
        for depth in depths:
            self.__update(depth[0], depth[1])
        self.__recalculate_totals(0)
        self.signal_changed.emit()

    def __slot_depth(self, price, volume):

        index = self.__update(price, volume)
        self.__recalculate_totals(index)
        self.signal_changed.emit()

    def __slot_ticker(self, bid, ask):

        if self.__typ == Market.TYPE_BID:
            self.__delete_all(bid)
        else:
            self.__delete_all(ask)

        self.__recalculate_totals(0)

        self.signal_changed.emit()

    def __update(self, price, volume):
        '''
        Updates the volume for the specified price.
        @return: the index of the affected level,
        or the index of the next higher level,
        if the affected level was deleted.
        '''
        (index, level) = self.__find_level(price)

        level.update(price, volume)
        if level.is_empty():
            self.__levels.remove(level)

        return index

    def __subtract(self, price, volume):
        '''
        Subtracts the volume for the specified price.
        or the index of the next higher level,
        if the affected level was deleted.
        '''
        (index, level) = self.__find_level(price)

        level.subtract(price, volume)
        if level.is_empty():
            self.__levels.remove(level)

        return index

    def __delete_all(self, price):
        '''
        Deletes all orders below (type ascending)
        or above (type descending) the specified price.
        '''
        levels = self.__levels
        compare = self.__compare

        while len(levels) != 0:
            level = levels[0]
            level.delete_all(compare, price)
            if level.size() == 0:
                levels.remove(level)
            else:
                break

    def __recalculate_totals(self, index):
        '''
        Recalculates the totals of all levels, starting at the specified index.
        '''
        levels = self.__levels

        if index == 0:
            total = 0
        else:
            total = levels[index - 1].total

        maximum = len(levels)
        for i in range(index, maximum):
            level = levels[i]
            total += level.volume
            level.total = total

    def __find_level(self, price):
        '''
        Finds the level for the specified price. If no level exists,
        inserts a new level at the correct position.
        Stolen from goxtool ;)
        @return: tuple (index, level)
        '''
        grouping = self.__grouping
        key = price / grouping * grouping
        if price % grouping != 0:
            key += grouping
        compare = self.__compare
        levels = self.__levels
        low = 0
        high = len(levels)

        # binary search
        while low < high:
            mid = (low + high) / 2
            midval = levels[mid].key
            if compare(midval, key):
                low = mid + 1
            elif compare(key, midval):
                high = mid
            else:
                return (mid, levels[mid])

        # not found - insert new level
        level = Level(key)
        self.__levels.insert(low, level)

        return (low, level)

    # public methods

    def size(self):
        '''
        Returns the number of levels in this collection.
        '''
        return len(self.__levels)

    def get_price(self, index):
        '''
        Returns the price at the specified level.
        '''
        return self.__levels[index].key

    def get_volume(self, index):
        '''
        Returns the volume at the specified level.
        '''
        return self.__levels[index].volume

    def get_total(self, index):
        '''
        Returns the total volume at the specified level.
        '''
        return self.__levels[index].total

    def get_quote(self, index):
        '''
        Returns the quote price for the level at the specified index.
        '''
        return money.multiply(self.get_price(index), self.get_volume(index))

    def get_total_quote(self, index):
        '''
        Returns the quote price for all levels up to the specified index.
        '''
        return money.multiply(self.get_price(index), self.get_total(index))

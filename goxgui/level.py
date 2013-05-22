class Level(object):
    '''
    Represents a level in an orders collection.
    '''
    def __init__(self, key):
        self.key = key
        self.items = {}
        self.volume = 0
        self.total = 0
        self.price = 0

    def update(self, price, volume):

        if volume <= 0:
            try:
                self.items.pop(price)
                if self.is_empty():
                    return
            except:
                return
        else:
            self.items[price] = volume

        self.__update()

    def subtract(self, price, volume):
        self.add(price, -volume)

    def add(self, price, volume):
        self.update(price, self.items.get(price, 0) + volume)

    def __update(self):

        self.volume = 0
        self.price = 0

        for price, volume in self.items.items():
            self.price += price
            self.volume += volume

        self.price /= self.size()

    def size(self):
        return len(self.items.keys())

    def is_empty(self):
        return self.size() == 0

    def delete_all(self, compare, limit):
        for price in sorted(self.items.keys()):
            if compare(price, limit):
                self.items.pop(price)
            else:
                self.__update()
                break

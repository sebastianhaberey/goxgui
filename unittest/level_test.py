import unittest
from money import to_money
from level import Level


class Test(unittest.TestCase):

    def test_construct(self):
        level = Level(23)
        self.assertEquals(23, level.key)
        self.assertEquals(0, level.volume)
        self.assertEquals(0, level.total)

    def test_update(self):
        level = Level(0)

        level.update(to_money(120), to_money(1))

        self.assertEquals(to_money(1), level.volume)
        self.assertEquals(to_money(120), level.price)

        level.update(to_money(121), to_money(1))

        self.assertEquals(to_money(2), level.volume)
        self.assertEquals(to_money(120.5), level.price)

        level.update(to_money(120), to_money(0))

        self.assertEquals(to_money(1), level.volume)
        self.assertEquals(to_money(121), level.price)

    def test_delete_all(self):
        level = Level(0)

        level.update(to_money(120), to_money(1))
        level.update(to_money(121), to_money(1))
        level.update(to_money(122), to_money(1))

        level.delete_all(lambda x, y: x < y, to_money(122))
        self.assertEquals(1, level.size())

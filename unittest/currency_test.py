import unittest
from currency import Currency


class Test(unittest.TestCase):

    def test_construct(self):
        currency = Currency('EUR')
        self.assertEquals('EUR', currency.symbol)
        self.assertEquals(5, currency.decimals)

    def test_equals(self):
        currencyA = Currency('EUR')
        currencyB = Currency('EUR')
        self.assertEquals(currencyA, currencyB)

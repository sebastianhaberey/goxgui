import unittest
from currency import Currency
import money


class Test(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(1000000000,
            money.multiply(200000000, 500000000))

    def test_divide(self):
        self.assertEqual(200000000,
            money.divide(1000000000, 500000000))

    def test_to_string(self):
        self.assertEquals('7,000.00000',
            money.to_string(700000000000, Currency('USD')))

    def test_to_long_string(self):
        self.assertEquals('2,000.00000 EUR',
            money.to_long_string(200000000000, Currency('EUR')))

    def test_to_float(self):
        self.assertEquals(6.0, money.to_float(600000000))

    def test_pip(self):
        self.assertEquals(1000, money.pip(Currency('USD')))

    def test_to_money(self):
        self.assertEquals(1550000000, money.to_money(15.5))

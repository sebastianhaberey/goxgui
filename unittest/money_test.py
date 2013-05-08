import unittest
from money import Money
from currency import Currency


class Test(unittest.TestCase):

    def test_construct(self):
        money = Money(1.0, Currency('USD'))
        self.assertEquals(100000000, money.value)
        self.assertEquals(Currency('USD'), money.currency)
        self.assertEquals('USD', money.symbol)
        self.assertEquals(5, money.decimals)

    def test_construct_noshift(self):
        money = Money(100000000, Currency('USD'), False)
        self.assertEquals(100000000, money.value)
        self.assertEquals(Currency('USD'), money.currency)
        self.assertEquals('USD', money.symbol)
        self.assertEquals(5, money.decimals)

    def test_multiply(self):

        moneyA = Money(10.0, Currency('USD'))
        moneyB = Money(5.0)
        moneyC = moneyA * moneyB

        # the result should have money A's properties
        self.assertEquals(5000000000, moneyC.value)
        self.assertEquals(Currency('USD'), moneyC.currency)
        self.assertEquals(5, moneyC.decimals)

        moneyA = Money(10.0)
        moneyB = Money(5.0, Currency('EUR'))
        moneyC = moneyA * moneyB

        # the result should have money A's properties
        self.assertEquals(5000000000, moneyC.value)
        self.assertEquals(Currency('BTC'), moneyC.currency)
        self.assertEquals(8, moneyC.decimals)

    def test_divide(self):

        moneyA = Money(10.0, Currency('USD'))
        moneyB = Money(5.0)
        moneyC = moneyA / moneyB

        self.assertEquals(200000000, moneyC.value)
        self.assertEquals(Currency('USD'), moneyC.currency)

    def test_add(self):

        moneyA = Money(10.0, Currency('USD'))
        moneyB = Money(5.0)
        moneyC = moneyA + moneyB

        self.assertEquals(1500000000, moneyC.value)
        self.assertEquals(Currency('USD'), moneyC.currency)

    def test_sub(self):

        moneyA = Money(10.0, Currency('USD'))
        moneyB = Money(5.0)
        moneyC = moneyA - moneyB

        self.assertEquals(500000000, moneyC.value)
        self.assertEquals(Currency('USD'), moneyC.currency)

    def test_to_string(self):
        money = Money(1000, Currency('USD'))
        self.assertEquals('1,000.00000', str(money))

    def test_to_float(self):
        money = Money(6, Currency('USD'))
        self.assertEquals(6.0, money.to_float())

    def test_to_long_string(self):
        money = Money(1000, Currency('EUR'))
        self.assertEquals('1,000.00000 EUR', money.to_long_string())

    def test_pip(self):
        money = Money(1, Currency('USD'))
        self.assertEquals(1000, money.pip().value)

    def test_change_type(self):

        money = Money(6666.6, Currency('USD'))

        self.assertEquals(6666.6, money.to_float())
        self.assertEquals('6,666.60000', str(money))
        self.assertEquals(Currency('USD'), money.currency)
        self.assertEquals(5, money.decimals)

        money.currency = Currency('JPY')

        self.assertEquals(6666.6, money.to_float())
        self.assertEquals('6,666.600', str(money))
        self.assertEquals(Currency('JPY'), money.currency)
        self.assertEquals(3, money.decimals)

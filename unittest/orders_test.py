import unittest
from orders import Orders
from money import to_money
from market import Market
from market_mock import MarketMock


class Test(unittest.TestCase):

    def setUp(self):
        self.market = MarketMock()

    def test_size(self):

        orders = Orders(self.market, Market.TYPE_ASK, 1)

        # group 0
        self.market.depth_ask(120.0, 1)
        self.assertEquals(1, orders.size())

        # group 1
        self.market.depth_ask(120.1, 1)
        self.assertEquals(2, orders.size())

        # group 1
        self.market.depth_ask(120.9, 1)
        self.assertEquals(2, orders.size())

        # group 1
        self.market.depth_ask(121.0, 1)
        self.assertEquals(2, orders.size())

        # group 2
        self.market.depth_ask(122.0, 1)
        self.assertEquals(3, orders.size())

    def test_grouping(self):

        orders = Orders(self.market, Market.TYPE_ASK, 0.6)

        # group 0
        self.market.depth_ask(0.0, 1)
        # group 1
        self.market.depth_ask(0.1, 1)
        self.market.depth_ask(0.3, 1)
        self.market.depth_ask(0.6, 1)
        self.assertEquals(2, orders.size())
        self.assertEquals(to_money(3), orders.get_volume(1))

        # group 2
        self.market.depth_ask(1.1, 1)
        self.market.depth_ask(1.2, 1)
        self.assertEquals(3, orders.size())

        # remove group 2
        self.market.depth_ask(1.1, 0)
        self.market.depth_ask(1.2, 0)
        self.assertEquals(2, orders.size())

    def test_no_grouping(self):

        orders = Orders(self.market, Market.TYPE_ASK)

        self.market.depth_ask(0.00000000, 1)
        self.market.depth_ask(0.00000001, 1)
        self.market.depth_ask(0.00000002, 1)

        self.assertEquals(3, orders.size())

    def test_grouping_price(self):

        orders = Orders(self.market, Market.TYPE_ASK, 1)

        # group 0
        self.market.depth_ask(120.0, 1)
        # group 1
        self.market.depth_ask(120.4, 1)
        self.market.depth_ask(121.0, 1)
        # group 2
        self.market.depth_ask(121.8, 1)

        self.assertEquals(to_money(120.0), orders.get_price(0))
        self.assertEquals(to_money(121.0), orders.get_price(1))
        self.assertEquals(to_money(122.0), orders.get_price(2))

    def test_remove_empty(self):

        orders = Orders(self.market, Market.TYPE_ASK, 1)

        self.market.depth_ask(120, 20)
        self.assertEquals(1, orders.size())

        self.market.depth_ask(120, 0)
        self.assertEquals(0, orders.size())

    def test_total(self):

        orders = Orders(self.market, Market.TYPE_ASK)

        self.market.depth_ask(10, 3)
        self.market.depth_ask(20, 2)
        self.market.depth_ask(30, 1)

        self.assertEquals(3, orders.size())

        self.assertEquals(to_money(3), orders.get_total(0))
        self.assertEquals(to_money(5), orders.get_total(1))
        self.assertEquals(to_money(6), orders.get_total(2))

    def test_depth_bid(self):

        orders = Orders(self.market, Market.TYPE_BID)

        self.market.depth_bid(10, 1)
        self.market.depth_bid(20, 1)
        self.market.depth_bid(30, 1)

        self.assertEquals(to_money(30), orders.get_price(0))
        self.assertEquals(to_money(20), orders.get_price(1))
        self.assertEquals(to_money(10), orders.get_price(2))

    def test_depth_ask(self):

        orders = Orders(self.market, Market.TYPE_ASK, 1)

        self.market.depth_ask(10, 1)
        self.market.depth_ask(20, 1)
        self.market.depth_ask(30, 1)

        self.assertEquals(to_money(10), orders.get_price(0))
        self.assertEquals(to_money(20), orders.get_price(1))
        self.assertEquals(to_money(30), orders.get_price(2))

    def test_ticker(self):

        ordersA = Orders(self.market, Market.TYPE_ASK)
        ordersB = Orders(self.market, Market.TYPE_BID)

        self.market.depth_bid(3.5, 1)
        self.market.depth_bid(3.3, 1)
        self.market.depth_bid(3.0, 1)
        self.market.depth_bid(2.2, 1)
        self.market.depth_bid(1.3, 1)
        self.market.depth_bid(1.0, 1)

        self.market.depth_ask(4.6, 1)
        self.market.depth_ask(5.0, 1)
        self.market.depth_ask(5.2, 1)
        self.market.depth_ask(6.0, 1)
        self.market.depth_ask(6.5, 1)

        self.market.ticker(3.0, 5.0)

        self.assertEquals(4, ordersA.size())
        self.assertEquals(to_money(5.0), ordersA.get_price(0))

        self.assertEquals(4, ordersB.size())
        self.assertEquals(to_money(3.0), ordersB.get_price(0))

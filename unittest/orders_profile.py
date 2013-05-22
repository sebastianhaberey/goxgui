from market import Market
from market_mock import MarketMock
from orders import Orders
import random
import unittest
import cProfile
import pstats


class Test(unittest.TestCase):

    COUNT = 10000

    def setUp(self):

        self.market = MarketMock()
        self.orders = Orders(self.market, Market.TYPE_ASK)

        self.profile = cProfile.Profile()
        self.profile.enable()

    def tearDown(self):

        self.profile.disable()
        stats = pstats.Stats(self.profile)
        stats.strip_dirs().sort_stats('time').print_stats(5)

    def test_profile_depth_ask_random(self):

        count = 0
        while count < self.COUNT:
            self.market.depth_ask(float(random.randint(0, 12000)) / 100, 1.0)
            count += 1

    def test_profile_depth_ask_sequence(self):

        count = 0
        while count < self.COUNT:
            self.market.depth_ask(float(count) / 100, 1.0)
            count += 1

    def test_profile_depth_asks_random(self):

        count = 0
        depths = []
        while count < self.COUNT:
            depths.append([float(random.randint(0, 12000)) / 100, 1.0])
            count += 1

        self.market.depth_asks(depths)

    def test_profile_depth_asks_sequence(self):

        count = 0
        depths = []
        while count < self.COUNT:
            depths.append([float(count) / 100, 1.0])
            count += 1

        self.market.depth_asks(depths)

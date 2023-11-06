import random
from datetime import datetime

import pandas as pd
from django.test import SimpleTestCase
from pandas import DataFrame

from quant_tick.lib import (
    aggregate_trades,
    get_current_time,
    get_min_time,
    get_runs,
    volume_filter_with_time_window,
)

from ..base import BaseRandomTradeTest


class TradeAggregatorTest(BaseRandomTradeTest, SimpleTestCase):
    def test_equal_symbols_and_timestamps_and_ticks(self):
        """Aggregated trades with equal symbols, timestamps, and ticks."""
        trades = [{"symbol": "A", "is_equal_timestamp": True, "ticks": [1, 1]}]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 1)

    def test_equal_symbols_and_timestamps_and_not_equal_ticks(self):
        """Aggregated trades with equal symbols and timestamps, but not equal ticks."""
        trades = [{"symbol": "A", "is_equal_timestamp": True, "ticks": [1, -1]}]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 2)

    def test_not_equal_symbols_and_equal_timestamps_and_ticks(self):
        """Aggregated trades with not equal symbols, but equal timestamps and ticks."""
        trades = [
            {"symbol": "A", "is_equal_timestamp": True, "ticks": [1, 1]},
            {"symbol": "B", "is_equal_timestamp": True, "ticks": [1, 1]},
        ]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 2)

    def test_not_equal_symbols_and_timestamps_and_equal_ticks(self):
        """Aggregated trades with not equal symbols or timestamps, but equal ticks."""
        trades = [
            {"symbol": "A", "is_equal_timestamp": True, "ticks": [1, 1]},
            {"symbol": "A", "is_equal_timestamp": False, "ticks": [-1]},
            {"symbol": "B", "is_equal_timestamp": True, "ticks": [1, 1]},
            {"symbol": "B", "is_equal_timestamp": False, "ticks": [-1]},
        ]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 4)

    def test_equal_ticks_and_equal_timestamp(self):
        """Aggregated trades with equal ticks and equal timestamp."""
        trades = [{"ticks": [1, 1], "is_equal_timestamp": True}]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 1)

    def test_equal_ticks_and_not_equal_timestamp(self):
        """Aggregated trades with equal ticks and not equal timestamp."""
        trades = [{"ticks": [1, 1], "is_equal_timestamp": False}]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 2)

    def test_equal_ticks_and_equal_nanoseconds(self):
        """Aggregated trades with equal ticks and equal nanoseconds."""
        trades = [
            {
                "ticks": [1, 1],
                "is_equal_timestamp": True,
                "nanoseconds": random.random() * 100,
            }
        ]
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 1)

    def test_equal_ticks_and_not_equal_nanoseconds(self):
        """Aggregated trades with equal ticks and not equal nanoseconds."""
        trades = []
        nanoseconds = random.random() * 100
        for index, tick in enumerate([1, 1]):
            nanoseconds += index
            trade = {
                "ticks": [tick],
                "is_equal_timestamp": True,
                "nanoseconds": nanoseconds,
            }
            trades.append(trade)
        data_frame = self.get_data_frame(trades)
        data = aggregate_trades(data_frame)
        self.assertEqual(len(data), 2)


class VolumeFilterTest(BaseRandomTradeTest, SimpleTestCase):
    def assert_min_volume(self, df: DataFrame) -> None:
        """Assert minimum volume."""
        assert isinstance(df.timestamp, datetime)
        assert_1 = ("price", "tickRule")
        assert_2 = ("volume", "notional", "ticks")
        self.assertTrue(all([df[key] == 1 for key in assert_1]))
        self.assertTrue(all([df[key] == 2 for key in assert_2]))

    def assert_not_min_volume(
        self, df: DataFrame, buy: int = 0, total: int = 2
    ) -> None:
        """Assert not minimum volume."""
        assert_1 = ("high", "low")
        assert_buy = ("totalBuyVolume", "totalBuyNotional", "totalBuyTicks")
        assert_total = ("totalVolume", "totalNotional", "totalTicks")
        self.assertTrue(all([df[key] == 1 for key in assert_1]))
        self.assertTrue(all([df[key] == buy for key in assert_buy]))
        self.assertTrue(all([df[key] == total for key in assert_total]))

    def test_volume_filter(self):
        """Aggregated trade 1 is minimum volume."""
        now = get_current_time()
        kwargs = {"price": 1, "notional": 1}
        trades = [
            self.get_random_trade(timestamp=now, tick_rule=-1, **kwargs),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("1s"), tick_rule=-1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("2s"), tick_rule=1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("2s"), tick_rule=1, **kwargs
            ),
        ]
        data_frame = pd.DataFrame(trades)
        aggregated = aggregate_trades(data_frame)
        filtered = volume_filter_with_time_window(aggregated, min_volume=2, window=None)
        self.assertEqual(len(filtered), 1)
        self.assert_min_volume(filtered.iloc[0])
        self.assert_not_min_volume(filtered.iloc[0], buy=2, total=4)

    def test_volume_filter_with_8_trades(self):
        """Aggregated trades 1 and 3 are minimum volume."""
        now = get_current_time()
        kwargs = {"price": 1, "notional": 1}
        trades = [
            self.get_random_trade(timestamp=now, tick_rule=1, **kwargs),
            self.get_random_trade(timestamp=now, tick_rule=1, **kwargs),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("1s"), tick_rule=-1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("2s"), tick_rule=-1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("3s"), tick_rule=1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("3s"), tick_rule=1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("4s"), tick_rule=-1, **kwargs
            ),
            self.get_random_trade(
                timestamp=now + pd.Timedelta("5s"), tick_rule=-1, **kwargs
            ),
        ]
        data_frame = pd.DataFrame(trades)
        aggregated = aggregate_trades(data_frame)
        filtered = volume_filter_with_time_window(aggregated, min_volume=2, window=None)
        self.assertEqual(len(filtered), 3)
        self.assert_min_volume(filtered.iloc[0])
        self.assert_min_volume(filtered.iloc[1])
        self.assert_not_min_volume(filtered.iloc[1], buy=2, total=4)
        self.assert_not_min_volume(filtered.iloc[2])

    def test_volume_filter_with_1_trade_exceeding_1m_window(self):
        """
        Aggregated trades, with trade 2 less than minimum volume,
        and trade 3 greater than window.
        """
        min_time = get_min_time(get_current_time(), "1d")
        one_second = pd.Timedelta("1s")
        one_minute = pd.Timedelta("1t")
        kwargs = {"price": 1, "notional": 1, "tick_rule": 1}
        trades = [
            self.get_random_trade(timestamp=min_time, **kwargs),
            self.get_random_trade(timestamp=min_time, **kwargs),
            self.get_random_trade(timestamp=min_time + one_second, **kwargs),
            self.get_random_trade(
                timestamp=min_time + one_minute + one_second, **kwargs
            ),
        ]
        data_frame = pd.DataFrame(trades)
        aggregated = aggregate_trades(data_frame)
        filtered = volume_filter_with_time_window(aggregated, min_volume=2, window="1t")
        self.assertEqual(len(filtered), 3)
        self.assert_min_volume(filtered.iloc[0])
        self.assert_not_min_volume(filtered.iloc[1], buy=1, total=1)
        self.assert_not_min_volume(filtered.iloc[2], buy=1, total=1)

    def test_volume_filter_with_2_trades_exceeding_1m_window(self):
        """
        Aggregated trades, with trade 2 less than minimum volume,
        and trade 3 and 4 greater than window.
        """
        min_time = get_min_time(get_current_time(), "1d")
        one_second = pd.Timedelta("1s")
        one_minute = pd.Timedelta("1t")
        kwargs = {"price": 1, "notional": 1, "tick_rule": 1}
        trades = [
            self.get_random_trade(timestamp=min_time, **kwargs),
            self.get_random_trade(timestamp=min_time, **kwargs),
            self.get_random_trade(timestamp=min_time + one_second, **kwargs),
            self.get_random_trade(
                timestamp=min_time + one_minute + one_second, **kwargs
            ),
            self.get_random_trade(
                timestamp=min_time + one_minute + one_second * 2, **kwargs
            ),
        ]
        data_frame = pd.DataFrame(trades)
        aggregated = aggregate_trades(data_frame)
        filtered = volume_filter_with_time_window(aggregated, min_volume=2, window="1t")
        self.assertEqual(len(filtered), 3)
        self.assert_min_volume(filtered.iloc[0])
        self.assert_not_min_volume(filtered.iloc[1], buy=1, total=1)
        self.assert_not_min_volume(filtered.iloc[2], buy=2, total=2)


class GetRunsTest(BaseRandomTradeTest, SimpleTestCase):
    def test_one_up_tick(self):
        """One up tick."""
        up = self.get_random_trade(tick_rule=1)
        data_frame = pd.DataFrame([up])
        runs = get_runs(data_frame)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["ticks"], 1)

    def test_one_up_tick_and_one_down_tick(self):
        """One up tick, and one down tick."""
        up = self.get_random_trade(tick_rule=1)
        down = self.get_random_trade(tick_rule=-1)
        data_frame = pd.DataFrame([up, down])
        runs = get_runs(data_frame)
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[0]["ticks"], 1)
        self.assertEqual(runs[1]["ticks"], -1)

    def test_one_up_tick_and_one_down_tick_with_runs_N(self):
        """One up tick and one down tick, with runs N of 2."""
        up = self.get_random_trade(tick_rule=1)
        down = self.get_random_trade(tick_rule=-1)
        data_frame = pd.DataFrame([up, down])
        runs = get_runs(data_frame, runs_n=2)
        self.assertEqual(len(runs), 0)

    def test_two_up_ticks_and_one_down_tick(self):
        """Two up ticks and one down tick."""
        up = self.get_random_trade(tick_rule=1)
        down = self.get_random_trade(tick_rule=-1)
        data_frame = pd.DataFrame(([up] * 2) + [down])
        runs = get_runs(data_frame)
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[0]["ticks"], 2)
        self.assertEqual(runs[1]["ticks"], -1)

    def test_two_up_ticks_and_one_down_tick_with_runs_N(self):
        """Two up ticks and one down tick, with runs N of 2."""
        up = self.get_random_trade(tick_rule=1)
        down = self.get_random_trade(tick_rule=-1)
        data_frame = pd.DataFrame(([up] * 2) + [down])
        runs = get_runs(data_frame, runs_n=2)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["ticks"], 2)

    def test_bins(self):
        """Bins 1, 2, 3."""
        trades = [
            self.get_random_trade(price=1, notional=i + 1, tick_rule=1)
            for i in range(3)
        ]
        data_frame = pd.DataFrame(trades)
        runs = get_runs(data_frame, bins=[1, 2, 3])
        self.assertEqual(len(runs), 1)
        for i in range(3):
            self.assertEqual(runs[0][f"volume{i + 1}"], 1)

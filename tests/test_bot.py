import pytest
from mm_bot import CoinstoreMMBot

@pytest.fixture
def bot():
    return CoinstoreMMBot()

def test_bot_initialization(bot):
    assert bot.symbol == 'BLM/USDT'
    assert bot.min_spread == 0.001
    assert bot.max_spread == 0.02
    assert bot.min_order_size == 100
    assert bot.max_order_size == 1000
    assert bot.order_count == 5

def test_calculate_volatility(bot):
    # Test with empty price history
    assert bot.calculate_volatility() == 0

    # Test with price history
    bot.price_history = [100, 101, 99, 102]
    volatility = bot.calculate_volatility()
    assert isinstance(volatility, float)
    assert volatility >= 0

def test_get_market_trend(bot):
    # Test with insufficient data
    assert bot.get_market_trend() == "neutral"

    # Test bullish trend
    bot.price_history = [100] * 10 + [110] * 10
    assert bot.get_market_trend() == "bullish"

    # Test bearish trend
    bot.price_history = [100] * 10 + [90] * 10
    assert bot.get_market_trend() == "bearish"

def test_calculate_dynamic_spread(bot):
    spread = bot.calculate_dynamic_spread("neutral")
    assert bot.min_spread <= spread <= bot.max_spread

    spread_bullish = bot.calculate_dynamic_spread("bullish")
    assert spread_bullish > spread

    spread_bearish = bot.calculate_dynamic_spread("bearish")
    assert spread_bearish < spread

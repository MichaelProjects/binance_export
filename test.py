import pytest

from app.lib.functions import in_out_transfer, coins_in_portfolio, evaluate_portfolio
from app.lib.calc import TimeframeUtils
from app.lib.parse_conf import set_env
from app.lib.binance_api import get_fiat_deposits, get_fit_withdraw, ping

set_env()


@pytest.mark.asyncio
async def test_in_out_transfer():
    timeframes = TimeframeUtils.calc_timeframes(TimeframeUtils.get_exchange_time())
    guv = await in_out_transfer(timeframes)
    assert guv != 0

@pytest.mark.asyncio
async def test_fiat_deposit():
    result = []
    timeframes = TimeframeUtils.calc_timeframes(TimeframeUtils.get_exchange_time())
    for timeframe in timeframes:
        response = await get_fiat_deposits(timeframe['start'], timeframe['end'])
        result.append(response)
    assert len(result) != 0

@pytest.mark.asyncio
async def test_fiat_withdraw():
    result = []
    timeframes = TimeframeUtils.calc_timeframes(TimeframeUtils.get_exchange_time())
    for timeframe in timeframes:
        response = await get_fit_withdraw(timeframe['start'], timeframe['end'])
        result.append(response)
    assert len(result) != 0

@pytest.mark.asyncio
async def test_coins_in_portfolio():
    coins = await coins_in_portfolio()
    assert len(coins) != 0

@pytest.mark.asyncio
async def test_evaluate_portfolio():
    coins = await coins_in_portfolio()
    amount = await evaluate_portfolio(coins)
    print(amount)

@pytest.mark.asyncio
def test_ping():
    response = ping()
    print(response)
    assert response != {}

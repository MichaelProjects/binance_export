from fastapi import Response, status, APIRouter, status, Depends

from app.lib.binance_api import ping
from app.lib.functions import evaluate_portfolio, coins_in_portfolio, in_out_transfer
from app.lib.calc import TimeframeUtils


v1_router = APIRouter(
    prefix="/api/v1/provider/binance",
    tags=["binance_endpoints"],
    responses={404: {"description": "Not found"}},
)

@v1_router.get("/health")
async def get_health(response: Response):
    pong = await ping()
    if pong != {}:
        response.status_code = status.HTTP523_SERVICE_UNAVAILABLE
        return {"code": 523, "status": "Binance API is not responding"}

    response.status_code = status.HTTP_200_OK
    return {"code": 200, "status": "OK"}


@v1_router.get("/account/analyse/{user_id}")
async def account_analyse(user_id: str):
    currency = "USDT"
    timeframes = TimeframeUtils.calc_timeframes(TimeframeUtils.get_exchange_time())
    coins = await coins_in_portfolio()
    response, failed_coins = await evaluate_portfolio(coins)
    brutto_balance = await in_out_transfer(timeframes)
    return {"portfolio_value": response, "failed_coins": failed_coins, "brutto_balance": brutto_balance, "currency": currency}

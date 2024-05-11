from app.lib.binance_api import get_coin_price

async def binance_is_weird(symbol: str, coin_amount: int) -> str:
    """
    Special rules for weird symbols that are difficult to request with the api.
    So we have to do it manually. If a symbol will be marked in the [failed_coin] it will be added here and rolled out in the next update.
    """
    if symbol == "BETHUSDT":
        response = await get_coin_price("BETHETH")
        price = float(response["price"])
        response = await get_coin_price("ETHUSDT")
        usdt_price = float(response["price"])
        return (coin_amount * price) * usdt_price
    
    return False

from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException
import os
import logging


async def get_client():
    return await AsyncClient.create(os.environ['public'], os.environ['private'])

async def get_coin_price(symbol: str) -> dict:
    response = False
    client = await get_client()
    try:
        response = await client.get_symbol_ticker(symbol=symbol)
    except BinanceAPIException as e:
        # if symbol does not exists
        if e.code == 1211:
            return False
    return response

async def order_history(end: float, start: float):
    client = await get_client()
    result = await client.get_all_orders(startTime=start, symbol="BTCUSDT")
    return result

async def withdraw_history_coins(start: float, end: float):
    client = await get_client()
    result = await client.get_withdraw_history(startTime=start, endTime=end)
    return result

async def deposit_history_coins(start: float, end: float):
    client = await get_client()
    result = await client.get_deposit_history(startTime=start, endTime=end)
    return result

async def get_portfolio() -> dict:
    client = await get_client()
    response = await client.get_account()
    logging.debug(response)
    return response

async def get_fiat_deposits(start: int, end: int):
    client = await get_client()
    response = await client.get_fiat_deposit_withdraw_history(transactionType="0", beginTime=start, endTime=end)
    return response

async def get_fit_withdraw(start: int, end: int):
    client = await get_client()
    response = await client.get_fiat_deposit_withdraw_history(transactionType="1", beginTime=start, endTime=end)
    return response

async def ping():
    client = await get_client()
    response = await client.ping()
    return response

from datetime import datetime
import logging

from app.lib.special_rules import binance_is_weird
from app.lib.binance_api import get_fiat_deposits, get_fit_withdraw, get_portfolio, get_coin_price

async def in_out_transfer(timeframes: list) -> float:
    value = 0
    fiat_currency = []
    for timeframe in timeframes:
        with_response = await get_fit_withdraw(timeframe['start'], timeframe['end'])
        dep_response = await get_fiat_deposits(timeframe['start'], timeframe['end'])
        logging.debug(f"Withdraw: {with_response}")
        logging.debug(f"Deposit: {dep_response}")

        if len(dep_response["data"]) != 0:
            for deposit in dep_response["data"]:
                value += float(deposit["amount"])
                fiat_currency.append({"type": "deposit", "currency": deposit["fiatCurrency"], "amount": deposit["amount"]})
        if len(with_response["data"]) != 0:
            for withdraw in with_response["data"]:
                value -= float(withdraw["amount"])
                fiat_currency.append({"type": "withdraw", "currency": deposit["fiatCurrency"], "amount": deposit["amount"]})

    return value


async def coins_in_portfolio() -> list:
    """
    uses the binance api client to get a snapshot of the portfolio and checks each symbol for owned coints, if the user ownes "locked" or "free" coins.
    They will be added to the [owned_coins] list.

    :return: [owned_coins] list
    """
    response = await get_portfolio()
    owned_coins = []
    if response["accountType"] == "SPOT":
        for symbol in response["balances"]:
            if symbol["free"] != "0" or symbol["locked"] != "0":
                owned_coins.append(symbol)
    return owned_coins


async def evaluate_portfolio(coins: list) -> float:
    """
    get all assets of the user account "SPOT Wallet" and calculates the value of the portfolio.
    """
    failed_coins = []
    current_value = 0.0

    to_fetch = []

    for coin in coins:
        coin_symbol = coin["asset"]

        if coin_symbol == "USDT" or coin_symbol == "BUSD":
            current_value += float(coin["free"]) + float(coin["locked"])
        else:
            coin_symbol = coin_symbol + "USDT"
            amount = float(coin["free"]) + float(coin["locked"])
            # if locked or free is 0 then it will be skipped
            if amount == 0:
                continue
            logging.debug(coin_symbol)
            price = await get_coin_price(coin_symbol)
            if price == False:
                failed_coins.append({"symbol": coin_symbol, "amount": amount})
                continue
            current_value += amount * float(price["price"])

    # iterates over each failed coin and tries to apply hand written rules for the symbols
    for failed_coin in failed_coins:
        result = await binance_is_weird(failed_coin["symbol"], failed_coin["amount"])
        if result != False:
            # if found, the failed coin will be removed from the failed coins
            current_value += result
            failed_coins.remove(failed_coin)

    return current_value, failed_coins

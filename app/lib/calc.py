from dataclasses import dataclass
from datetime import timedelta, date, datetime
import datetime
import logging
from time import time
from binance.client import Client
import os
from .binance_api import order_history

@dataclass(init=True)
class TimeframeUtils:
    @staticmethod
    def calc_timeframes(exchange_time: float):
        timeframes = []
        start = date.fromtimestamp(exchange_time)
        logging.debug(start)
        # that are roughly about 5 years
        for i in range(20):
            end = start - timedelta(days=90)
            # convert from date to datetime
            start_form = datetime.datetime.strptime(str(start), '%Y-%m-%d')
            end_form = datetime.datetime.strptime(str(end), '%Y-%m-%d')
            # convert datetime to timestamp and append to results
            start_time = datetime.datetime.timestamp(start_form)
            end_time = datetime.datetime.timestamp(end_form)
            timeframes.append({"end": int(datetime.datetime.utcfromtimestamp(start_time).timestamp() * 1000), "start": int(datetime.datetime.utcfromtimestamp(end_time).timestamp() * 1000)})
            start = end
        logging.debug(timeframes)
        return timeframes

    @staticmethod
    def apply_timeframes(timeframes: list):
        transactions = []
        for timeframe in timeframes:
            logging.debug(f"Current timeframe: {timeframe}")
            result = order_history(timeframe[0], timeframe[1])
            transactions.append(result)

        return transactions

    @staticmethod
    def get_exchange_time():
        client = Client(os.environ['public'], os.environ['private'])
        exchange_info = client.get_exchange_info()["serverTime"]
        logging.debug(f"Binance-Exchange-Time: {exchange_info}")
        cutted_time = float(str(exchange_info)[:-3])
        return cutted_time

        
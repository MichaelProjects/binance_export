from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException
import os
import pytest

from app.lib.parse_conf import set_env
set_env()

@pytest.mark.asyncio
async def test_get_client():
    client = await AsyncClient.create(os.environ['public'], os.environ['private'])

    assert False
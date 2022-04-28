

import asyncio
from mt5_adapter.client import MTClient
from mt5_adapter.trade import *
from timeit import default_timer as timer
from mt5_adapter.model import TradeRequest
from mt5_adapter.wrappers import timing
from mt5_adapter.log import my_logger

symbol = "EURUSD"

# @timing


async def test_buy(client):
    await open_buy(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=123)

# @timing


async def test_sell(client):
    await open_sell(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=321)


# @timing
async def test_modify(client):
    await position_modify(metatrader=client, ticket=27864579, take_profit=1.0951, stop_loss=1.051)


@timing
async def test_close(client):
    await position_close(metatrader=client, ticket=27856480)


@timing
async def test_positions_get(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol, filter_magic=22)
    print(len(positions))


async def close_all_fast(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol)
    closed = [position_close(metatrader=client, ticket=position.ticket)
              for position in positions]
    await asyncio.gather(*closed)


async def close_all_slow(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol)
    for pos in positions:
        await position_close(metatrader=client, ticket=pos.ticket)


async def open_n_fast(client, n):
    buys = [test_buy(client) for _ in range(n)]
    sells = [test_sell(client) for _ in range(n)]
    await asyncio.gather(*buys, *sells)


async def open_n_slow(client, n):
    for _ in range(n):
        await test_buy(client)
        await test_sell(client)


@timing
async def get_symbol_info_slow(client: MTClient, symbol_list):

    symbol_list = await client.symbols_get("*")

    symbols = [await client.symbol_info(symbol.name) for symbol in symbol_list]
    my_logger.info(f"len symbols: {len(symbols)}")


@timing
async def get_symbol_info_fast(client: MTClient, symbol_list):
    symbol_list = await client.symbols_get("*")
    symbols = [client.symbol_info(symbol.name) for symbol in symbol_list]
    await asyncio.gather(*symbols)
    my_logger.info(f"len symbols: {len(symbols)}")


async def run_tests():
    client = MTClient()
    await client.initialize()

    await test_positions_get(client=client)

    await close_all_fast(client)

    await client.shutdown()


if __name__ == "__main__":
    asyncio.run(run_tests())

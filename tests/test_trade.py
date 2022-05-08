

import asyncio
from contextlib import closing
from pydoc import cli
from urllib import response
from mt5_adapter.client import MTClient
from mt5_adapter.trade import *
from timeit import default_timer as timer
from mt5_adapter.model import TradeRequest
from mt5_adapter.wrappers import timing
from mt5_adapter.log import my_logger

symbol = "EURUSD"

# @timing


async def test_buy(client):
    buy_result = await open_buy(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=123)
    #my_logger.debug(f"buy_result: {buy_result}")

async def test_sell(client):
    sell_result = await open_sell(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=321)

async def test_modify(client):
    modify_result = await position_modify(metatrader=client, ticket=27864579, take_profit=1.0951, stop_loss=1.051)

async def test_close(client,ticket:int):
    close_result =  await position_close(metatrader=client, ticket=ticket)


@timing
async def test_positions_get(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol, filter_magic=1)
    
    json_obj = [json.loads(pos.json()) for pos in positions] 
    
    my_logger.info(json.dumps(json_obj,indent=2))

@timing
async def test_close_all_fast(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol)
    closed = [position_close(metatrader=client, ticket=position.ticket) for position in positions]
    closed = await asyncio.gather(*closed)


async def test_close_all_slow(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol)
    for pos in positions:
        await position_close(metatrader=client, ticket=pos.ticket)
 

@timing
async def test_open_n_fast(client, n):
    buys = [open_buy(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=123) for _ in range(n)]
    sells = [open_sell(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=321) for _ in range(n)]
    results = await asyncio.gather(*buys, *sells)
    #my_logger.debug(f"results: {results}")


@timing
async def test_open_n_slow(client, n):
    results = []
    for _ in range(n):
        res = await test_buy(client)
        res = await test_sell(client)

    #my_logger.debug(f"results: {results}")

async def test_position_get_by_ticket(client):
    positions = await positions_get_all(metatrader=client, symbol=symbol)
    results = []
    for position in positions:
        res = await position_get_by_ticket(client,position.ticket)
        results.append(res)
    #my_logger.debug(f"res: {res}")  
    


async def run_tests():
    client = MTClient()
    await client.initialize()

    #await test_close_all_fast(client)
    #await test_position_get_by_ticket(client)
    #await test_close(client,ticket=27928776)
    #await test_close_all_slow(client)
    #await test_open_n_fast(client,10)
    #await test_open_n_fast(client,3)
    #await test_open_n_slow(client,2)
    await test_positions_get(client)
    #await test_buy(client)
    #await test_sell(client)
    #await test_close_all_fast(client=client)


   
    await client.shutdown()


if __name__ == "__main__":
    asyncio.run(run_tests())

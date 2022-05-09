import asyncio
from mt5_adapter.history import *
from mt5_adapter.log import my_logger
import json



_ticket = 27953964

async def test_closed_trade(client):
    closed = await get_closed_trade(client=client,ticket=_ticket)
    my_logger.debug(f"type(closed) = {type(closed)}")



async def test_closed_trades(client):
    result = await get_closed_trades(client=client,group="EURJPY")
    my_logger.debug(f"len(result) = {len(result)}  ---  type(result) = {type(result[0])}")


async def history_deals(client):
    result = await history_deals_by_date_group(client=client)
    my_logger.debug(f"len(result) = {len(result)}  ---  type(result) = {type(result[0])}")


async def history_orders(client):
    result = await history_orders_by_date_group(client=client)
    my_logger.debug(f"len(result) = {len(result)}  ---  type(result) = {type(result[0])}")

async def run_tests():
    client = MTClient()
    await client.initialize()
    
    #await test_closed_trade(client)
    await test_closed_trades(client)
    #await history_deals(client)
    #await history_orders(client)

    await client.shutdown()


if __name__ == "__main__":
    asyncio.run(run_tests())

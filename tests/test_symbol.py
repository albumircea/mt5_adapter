


import asyncio

from mt5_adapter.client import MTClient
from mt5_adapter.config import main_terminal_path
from mt5_adapter.symbol import get_symbol_info


async def test_get_symbol_info(client:MTClient):
    await get_symbol_info(client,"EURUSD")


async def run():
    client = MTClient()
    await client.initialize(path = main_terminal_path)
    await test_get_symbol_info(client)



if __name__ == "__main__":
    asyncio.run(run())

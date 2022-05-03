import asyncio
from mt5_adapter.model import *
from mt5_adapter.client import MTClient


async def main():
    client = MTClient()
    await client.initialize()
    t =await client.symbol_info_tick("EURUSD")
    tick = MTTick.from_mt_obj(t)




if __name__ == "__main__":
   asyncio.run(main())
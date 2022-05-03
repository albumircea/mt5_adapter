import asyncio
from datetime import datetime
from mt5_adapter.terminal import get_terminal_info_raw
from mt5_adapter.client import MTClient
from mt5_adapter.log import my_logger

async def test_info(client:MTClient):
    info= await client.symbol_info("EURUSD")
    time  = info.time
    time = datetime.fromtimestamp(time)
    my_logger.debug(f"time : {time} ")

async def run():
    client = MTClient()



    await client.initialize()
    await test_info(client)




if __name__ =="__main__":
    asyncio.run(run())
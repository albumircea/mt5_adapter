import asyncio
from datetime import datetime
from mt5_adapter.account import get_account_info, get_account_info_raw
from mt5_adapter.client import MTClient
from mt5_adapter.log import my_logger
import json



async def test_account(client:MTClient):

    info= await get_account_info(client)
    json_obj  = json.loads(info.json())

    my_logger.info(json.dumps(json_obj,indent=2))

    info2 = await get_account_info_raw(client)
    my_logger.info(info2)

async def run():
    client = MTClient()



    await client.initialize()
    await test_account(client)




if __name__ =="__main__":
    asyncio.run(run())
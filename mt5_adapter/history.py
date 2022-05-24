
import asyncio
from datetime import datetime, timedelta
import json
from typing import List
from mt5_adapter.client import MTClient,_mt5
from mt5_adapter.log import my_logger
from mt5_adapter.model import MTClosedTrade, MTDeal,MTOrder
from collections import Counter



async def get_closed_trade(client:MTClient,ticket):    
    return MTClosedTrade.from_mt_obj(
        mt_deal=await client.history_deal_get_by_ticket(ticket),
        mt_order=await client.history_order_get_by_ticket(ticket))

async def get_closed_trades(client:MTClient,date_from=datetime(2000,1,1),date_to=datetime.now()+timedelta(days=1),group="*")->List[MTClosedTrade]:
    

    deals =  await client.history_deals_get_by_date(date_from=date_from,date_to=date_to,group=group)
 
    position_ids = []
    for deal in deals:
        position_ids.append(deal.position_id)
    
    counter = Counter(position_ids)
    tasks = []
    for id in counter:
        if counter[id] == 2:
            tasks.append(get_closed_trade(client=client,ticket=id))

    return  await asyncio.gather(*tasks)
     



async def history_orders_by_date_group(client:MTClient,date_from=datetime(2000,1,1),date_to=datetime.now(),group="*"):
    orders = await client.history_orders_get_by_date(date_from=date_from,date_to=date_to,group=group)
    return orders


async def history_deals_by_date_group(client:MTClient,date_from=datetime(2000,1,1),date_to=datetime.now(),group="*"):
    deals = await client.history_deals_get_by_date(date_from=date_from,date_to=date_to,group=group)
    return deals

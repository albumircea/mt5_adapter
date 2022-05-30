
import math
from mt5_adapter.config import main_terminal_path, terminal_paths
from mt5_adapter.client import MTClient
from mt5_adapter.trade import *
import asyncio

from mt5_adapter.utils import chunks
terminal_workers: MTClient = []

def modify_order_dict(ticket: int, stop_loss: float = None, take_profit: float = None):
        return {
            "ticket":ticket,
            "stop_loss":stop_loss,
            "take_profit": take_profit
        }

async def initialize_workers():
    global terminal_workers
    for _ in range(len(terminal_paths)):
        terminal_workers.append(MTClient())
    index = 0
    for terminal in terminal_workers:
        await terminal.initialize(terminal_paths[index])
        index += 1

async def parallel_modify(function_list):
    global terminal_workers
    chunk_number = len(function_list)/len(terminal_workers)
    chunk_number = int(math.ceil(chunk_number))
    list_chunks = chunks(function_list,len(terminal_workers))
    tasks = []
    if len(terminal_workers) >= len(list_chunks):
        
        for _list,_terminal in zip(list_chunks,terminal_workers):
            for dic in _list:
                tasks.append(position_modify(metatrader=_terminal,ticket=dic["ticket"], stop_loss=dic["stop_loss"],take_profit=dic["take_profit"]))

    else:
        my_logger.error(f"Something went wrong")
        return

    
    results = await asyncio.gather(*tasks)
    return results 
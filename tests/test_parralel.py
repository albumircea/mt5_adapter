import asyncio
from mt5_adapter.trade_parallel import *
from mt5_adapter.trade import *
from mt5_adapter.terminal import get_terminal_info




_symbol = "EURUSD"
_magic   = 412
_metatrader:MTClient
tp_price = 1.06

async def main(terminal):
    buy_orders = []
    sell_orders = []
    ongoing_orders = await positions_get_all(metatrader=terminal, symbol=_symbol, filter_magic=_magic)
    if len(ongoing_orders) > 0:
        for pos in ongoing_orders:
            if pos.type == ORDER_TYPE.BUY:
                buy_orders.append(pos)
            elif pos.type == ORDER_TYPE.SELL:
                sell_orders.append(pos)
    
    
    modify_list = []
    for pos in sell_orders:
        modify_list.append(modify_order_dict(ticket=pos.ticket,
                                take_profit=tp_price))
    await parallel_modify(modify_list)


async def run_tests():
    _metatrader = MTClient()
    await _metatrader.initialize(path=main_terminal_path)
    await initialize_workers()
    await main(_metatrader)



if __name__ == "__main__":

    asyncio.run(run_tests())
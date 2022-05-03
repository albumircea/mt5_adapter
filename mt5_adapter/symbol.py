from typing import Union
from mt5_adapter.client import MTClient
from mt5_adapter.model import MTSymbol, MTTick
from mt5_adapter.log import my_logger


async def get_symbol_info_raw(metatrader: MTClient, symbol: str):
    return await metatrader.symbol_info(symbol=symbol)


async def get_symbol_info(metatrader: MTClient, symbol: str) -> Union[MTSymbol, None]:

    symbol_info = await metatrader.symbol_info(symbol=symbol)
    if symbol_info:
        symbol = MTSymbol()
        symbol.map_attributes_from_mt_object(symbol_info)
        return symbol
    return None


async def get_tick(metatrader: MTClient, symbol: str) -> Union[MTTick, None]:

    info_tick = await metatrader.symbol_info_tick(symbol)
    if info_tick:
        tick = MTTick()
        tick.from_mt_object(info_tick)
        return tick
    return None

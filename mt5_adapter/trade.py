
import json
import time
from typing import List, Union
from mt5_adapter.client import MTClient
from mt5_adapter.model import MTPosition, TradeRequest
from mt5_adapter.constant import ORDER_TYPE, TRADE_ACTION, POSITION_TYPE, TRADE_RETCODE
from mt5_adapter.config import splippage, retries_counter
from mt5_adapter.log import my_logger, LogJson


async def order_send(metatrader: MTClient, request: TradeRequest):
    try:
        response = await metatrader.order_send(request.get_dict())
    except Exception as ex:
        if my_logger:
            my_logger.error(LogJson('EXCEPTION', {
                'type': 'exception',
                        'last_error': await metatrader.last_error(),
                        'exception': {
                            'type': type(ex).__name__,
                            'message': str(ex),
                        },
                'call_signature': dict(function=metatrader.order_send.__name__, kwargs=request)
            }))
    return response

"""
PROCESS TRADES
"""


async def process_trade(metatrader: MTClient, request: TradeRequest):

    response = await order_send(metatrader, request)
    if not response:
        my_logger.critical(f"NO RESPONSE, possible bad request: {request}")
        return
    my_logger.info("TRADE RESPONSE : {response}")
    if response.retcode == TRADE_RETCODE.DONE:
        if request.type in [ORDER_TYPE.BUY, ORDER_TYPE.SELL]:
            position = MTPosition.from_mt_obj(await position_get_by_ticket(metatrader=metatrader, ticket=response.order))
            return position

    if response.retcode in [TRADE_RETCODE.REQUOTE, TRADE_RETCODE.PRICE_OFF]:
        retries = 1
        while retries < retries_counter:
            tick = await metatrader.symbol_info_tick(request.symbol)
            if request.type == ORDER_TYPE.BUY:
                request.price = tick.ask
            elif request.type == ORDER_TYPE.SELL:
                request.price = tick.bid

            response = await order_send(metatrader=metatrader, request=request)
            if response.retcode == TRADE_RETCODE.DONE:
                if request.type in [ORDER_TYPE.BUY, ORDER_TYPE.SELL]:
                    position = MTPosition.from_mt_obj(await position_get_by_ticket(metatrader=metatrader, ticket=response.order))
                    return position
            retries += 1
            time.sleep(0.1)
    return response


async def process_close(metatrader: MTClient, request: TradeRequest) -> bool:
    response = await order_send(metatrader, request)
    if not response:
        my_logger.critical(f"NO RESPONSE, possible bad request: {request}")
        return None

    my_logger.info("CLOSE RESPONSE : {response}")

    if response.retcode == TRADE_RETCODE.DONE:
        return True
    return False


async def process_modify(metatrader: MTClient, request: TradeRequest) -> bool:
    response = await order_send(metatrader, request)

    if not response:
        my_logger.critical(f"NO RESPONSE, possible bad request: {request}")
        return None

    my_logger.info("MODIFY RESPONSE : {response}")

    if response.retcode == TRADE_RETCODE.DONE:
        return True
    return False

"""
EXECUTE
"""


async def open_buy(
    metatrader: MTClient,
    symbol_name: str,
    volume: float,
    stop_loss: float = None,
    take_profit: float = None,
    magic_number: int = None,
    comment: str = None
) -> Union[MTPosition, None]:
    symbol_info = await metatrader.symbol_info(symbol=symbol_name)

    if symbol_info is not None:
        volume_ = volume if volume >= symbol_info.volume_min and volume <= symbol_info.volume_max else symbol_info.volume_min if volume < symbol_info.volume_min else symbol_info.volume_max

    sl_ = min(stop_loss, symbol_info.bid - symbol_info.trade_stops_level * symbol_info.point) if stop_loss else None
    tp_ = max(take_profit, symbol_info.bid + symbol_info.trade_stops_level * symbol_info.point) if take_profit else None

    request = TradeRequest(
        action=TRADE_ACTION.DEAL,
        symbol=symbol_name,
        magic=magic_number,
        type=ORDER_TYPE.BUY,
        volume=volume_,
        price=symbol_info.ask,
        sl=sl_,
        tp=tp_,
        deviation=float(splippage),
        comment=comment,
    )

    response = await process_trade(metatrader, request)
    return response


async def open_sell(
    metatrader: MTClient,
    symbol_name: str,
    volume: float,
    stop_loss: float = None,
    take_profit: float = None,
    magic_number: int = None,
    comment: str = None
) -> Union[MTPosition, None]:
    symbol_info = await metatrader.symbol_info(symbol=symbol_name)
    if symbol_info is not None:
        volume_ = volume if volume >= symbol_info.volume_min and volume <= symbol_info.volume_max else symbol_info.volume_min if volume < symbol_info.volume_min else symbol_info.volume_max

    sl_ = max(stop_loss, symbol_info.ask + symbol_info.trade_stops_level * symbol_info.point) if stop_loss else None
    tp_ = min(take_profit, symbol_info.ask - symbol_info.trade_stops_level * symbol_info.point) if take_profit else None

    request = TradeRequest(
        action=TRADE_ACTION.DEAL,
        symbol=symbol_name,
        magic=magic_number,
        type=ORDER_TYPE.SELL,
        volume=volume_,
        price=symbol_info.bid,
        sl=sl_,
        tp=tp_,
        deviation=splippage,
        comment=comment,
    )
    response = await process_trade(metatrader, request)
    return response


async def position_modify(
    metatrader: MTClient,
    ticket: int,
    stop_loss: float = None,
    take_profit: float = None
) -> bool:

    to_modify = await position_get_by_ticket(metatrader=metatrader, ticket=ticket)
    if not to_modify:
        return False

    symbol_info = await metatrader.symbol_info(symbol=to_modify.symbol)

    price = [symbol_info.ask, symbol_info.bid]
    sl_, tp_ = stop_loss, take_profit
    if stop_loss and stop_loss != to_modify.sl:
        if abs(stop_loss - price[int(abs(1 - to_modify.type % 2))]) < symbol_info.trade_stops_level * symbol_info.point:
            if to_modify.type == POSITION_TYPE.BUY:
                sl_ = price[0] - symbol_info.trade_stops_level * symbol_info.point
            if to_modify.type == POSITION_TYPE.SELL:
                sl_ = price[1] + symbol_info.trade_stops_level * symbol_info.point

    if take_profit and take_profit != to_modify.tp:
        if abs(take_profit - price[int(abs(1 - to_modify.type % 2))]) < symbol_info.trade_stops_level * symbol_info.point:
            if to_modify.type == POSITION_TYPE.BUY:
                tp_ = price[0] + symbol_info.trade_stops_level * symbol_info.point

            if to_modify.type == POSITION_TYPE.SELL:
                tp_ = price[1] - symbol_info.trade_stops_level * symbol_info.point

    if sl_ != to_modify.sl or tp_ != to_modify.tp:
        request = TradeRequest(
            action=TRADE_ACTION.SLTP,
            position=to_modify.ticket,
            symbol=to_modify.symbol,
            magic=to_modify.magic,
            sl=sl_,
            tp=tp_
        )
    response = await process_modify(metatrader, request)
    return response


async def position_close(metatrader: MTClient, ticket: int, to_close_volume: float = None):
    to_close = await position_get_by_ticket(metatrader, ticket)

    if to_close is None:
        my_logger.debug(f"Position could not be selected - ticket: {ticket}")
        return
    tick = await metatrader.symbol_info_tick(to_close.symbol)

    request = TradeRequest(
        action=TRADE_ACTION.DEAL,
        position=to_close.ticket,
        symbol=to_close.symbol,
        magic=to_close.magic,
        volume=to_close_volume if to_close_volume is not None else to_close.volume,
        deviation=splippage,
        type=abs(1 - to_close.type % 2),
        price=tick.ask if to_close.type == ORDER_TYPE.SELL else tick.bid
    )
    response = await process_close(metatrader, request)
    return response


async def position_get_by_ticket(metatrader: MTClient, ticket: int) -> MTPosition:
    try:
        position = await metatrader.position_get_by_ticket(ticket=ticket)
    except Exception as ex:
        if my_logger:
            my_logger.error(LogJson('EXCEPTION', {
                'type': 'exception',
                        'last_error': await metatrader.last_error(),
                        'exception': {
                            'type': type(ex).__name__,
                            'message': str(ex),
                        },
                'call_signature': dict(function=metatrader.order_send.__name__, kwargs=ticket.dict)
            }))

    if position is not None and len(position) == 1:
        return position[0] if position else None


async def positions_get_all(metatrader: MTClient, symbol: str = None, group: str = None, filter_magic=None) -> List[MTPosition]:
    if filter_magic:
        return [MTPosition.from_mt_obj(position) for position in await metatrader.positions_get(symbol=symbol, group=group) if position.magic == filter_magic]
    return [MTPosition.from_mt_obj(position) for position in await metatrader.positions_get(symbol=symbol, group=group)]

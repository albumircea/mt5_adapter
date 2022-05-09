from tkinter import N
from typing import Tuple
import pydantic
import datetime


class Base(pydantic.BaseModel):
    class Config:
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat(),
        }

    def get_dict(self):
        dic = {}
        for k in self.__dict__.keys():
            v = getattr(self, k)
            if v is not None:
                dic[k] = v
        return dic

    def from_mt_object(self, mt_object: Tuple):
        for k in self.__dict__.keys():
            v = getattr(mt_object, k)
            if v is not None:
                setattr(self, k, v)


class TradeRequest(Base):
    action: int = None  # Trade operation type
    magic: int = None
    order: int = None  # Order ticket
    symbol: str = None
    volume: float = None
    price: float = None
    stoplimit: float = None  # StopLimit level of the order
    sl: float = None
    tp: float = None
    deviation: int = None  # Maximal possible deviation from the requested price
    type: int = None
    typee_filling: int = None  # Order execution type
    type_time: int = None  # Order expiration type
    expiration: datetime.datetime = None  # Order expiration time (for the orders of ORDER_TIME_SPECIFIED type)
    comment: str = None
    position: int = None  # Position ticket
    position_by: int = None  # The ticket of an opposite position


class TradeResult(Base):
    retcode: int = None
    deal: int = None  # Deal ticket, if it is performed
    order: int = None  # Order ticket, if it is placed
    volume: float = None
    price: float = None
    bid: float = None
    ask: float = None
    comment: str = None
    request_id: int = None  # Request ID set by the terminal during the dispatch
    retcode_external: int = None  # Return code of an external trading system
    request: TradeRequest = None  # TradeRequest


class TradeCheckResult(Base):
    retcode: int = None
    balance: float = None
    equity: float = None
    profit: float = None
    margin: float = None
    margin_free: float = None
    margin_level: float = None
    comment: float = None


class MTTick(Base):
    ask: float = None
    bid: float = None
    flags: int = None
    last: float = None
    time_msc: int = None
    volume: float = None
    volume_real: float = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            ask=mt_obj.ask,
            bid=mt_obj.bid
        )


class MTSymbol(Base):
    ask: float = None
    bid: float = None
    spread: int = None
    digits: int = None
    point: float = None
    select: bool = None
    volume: float = None
    trade_tick_size: float = None
    trade_tick_value: float = None
    trade_stops_level: int = None
    volume_min: float = None
    volume_max: float = None
    #volume_step: float = None
    #category: str = None
    name: str = None
    time: datetime.datetime = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            ask=mt_obj.ask,
            bid=mt_obj.bid,
            spread=mt_obj.spread,
            digits=mt_obj.digits,
            point=mt_obj.point,
            select=mt_obj.select,
            volume=mt_obj.volume,
            trade_tick_size=mt_obj.trade_tick_size,
            trade_tick_value=mt_obj.trade_tick_value,
            trade_stops_level=mt_obj.trade_stops_level,
            volume_min=mt_obj.volume_min,
            volume_max=mt_obj.volume_max,
            name=mt_obj.name,
            time=datetime.datetime.fromtimestamp(mt_obj.time)
        )


class MTOrder(Base):
    magic: int = None
    ticket: int = None
    symbol: str = None
    type: int = None
    price_open: float = None
    comment: str = None
    sl: float = None
    tp: float = None
    volume_current: float = None
    volume_initial: float = None
    type_filling: int = None
    state: int = None
    time_setup: datetime.datetime = None
    position_id:int = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            magic=mt_obj.magic,
            ticket=mt_obj.ticket,
            symbol=mt_obj.symbol,
            type=mt_obj.type,
            price_open=mt_obj.price_open,
            comment=mt_obj.comment,
            sl=mt_obj.sl,
            tp=mt_obj.tp,
            volume_current=mt_obj.volume_current,
            volume_initial=mt_obj.volume_initial,
            type_filling=mt_obj.type_filling,
            state=mt_obj.state,
            time_setup=datetime.datetime.fromtimestamp(mt_obj.time_setup),
            position_id= mt_obj.position_id
        )


class MTDeal(Base):
    magic: int = None
    order: int = None
    position_id: int = None
    entry: int = None
    type: int = None
    reason: int = None
    commission: float = None  # doar aici am comisionul
    swap: float = None
    fee: float = None
    volume: float = None
    profit: float = None
    symbol: str = None
    comment: str = None
    time: datetime.datetime = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            magic=mt_obj.magic,
            order=mt_obj.order,
            position_id=mt_obj.position_id,
            entry=mt_obj.entry,
            type=mt_obj.type,
            commission=mt_obj.commission,
            swap=mt_obj.swap,
            volume=mt_obj.volume,
            profit=mt_obj.profit,
            symbol=mt_obj.symbol,
            comment=mt_obj.comment,
            time=datetime.datetime.fromtimestamp(mt_obj.time)
        )


class MTPosition(Base):
    magic: int = None
    type: int = None
    ticket: int = None
    identifier: int = None
    reason: int = None
    volume: float = None
    price_open: float = None
    sl: float = None
    tp: float = None
    swap: float = None
    profit: float = None
    symbol: str = None
    comment: str = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            magic=mt_obj.magic,
            type=mt_obj.type,
            ticket=mt_obj.ticket,
            identifier=mt_obj.identifier,
            reason=mt_obj.reason,
            volume=mt_obj.volume,
            price_open=mt_obj.price_open,
            sl=mt_obj.sl,
            tp=mt_obj.tp,
            swap=mt_obj.swap,
            profit=mt_obj.profit,
            symbol=mt_obj.symbol,
            comment=mt_obj.comment
        )


class MTClosedTrade(Base):
    ticket: int = None
    symbol: str = None
    type: int = None
    price_open: float = None
    price_close: float = None
    profit: float = None
    swap: float = None
    commission: float = None
    volume: float = None
    comment: str = None
    magic: int = None
    open_time: datetime.datetime = None
    close_time: datetime.datetime = None
    sl: float = None
    tp: float = None

    @classmethod
    def from_mt_obj(cls, mt_deal, mt_order):
        return cls(
            ticket=mt_order[0].ticket,
            symbol=mt_order[0].symbol,
            type=mt_order[0].type,
            price_open=mt_deal[0].price,
            price_close=mt_deal[1].price,
            profit=mt_deal[1].profit,
            swap=mt_deal[1].swap,
            commission=mt_deal[1].commission,
            comment = mt_order[0].comment,
            volume=mt_deal[1].volume,
            magic=mt_order[0].magic,
            open_time= datetime.datetime.fromtimestamp(mt_order[0].time_setup),
            close_time= datetime.datetime.fromtimestamp(mt_order[1].time_setup),
            sl=mt_order[0].sl if mt_order[1].sl == 0 else mt_order[1].sl,
            tp=mt_order[0].tp if mt_order[1].tp == 0 else mt_order[1].tp
        )


class MTAccount(Base):
    login: int = None
    leverage: int = None
    trade_allowed: bool = None
    trade_expert: bool = None
    trade_mode: int = None

    limit_orders: int = None

    margin_mode: int = None
    margin_so_mode: int = None
    margin: float = None
    margin_free: float = None
    margin_so_so: float = None
    margin_initial: float = None
    margin_level: float = None

    equity: float = None
    balance: float = None
    profit: float = None
    credit: float = None

    name: str = None
    server: str = None
    currency: str = None
    company: str = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            login=mt_obj.login,
            leverage=mt_obj.leverage,
            trade_allowed=mt_obj.trade_allowed,
            trade_expert=mt_obj.trade_expert,
            trade_mode=mt_obj.trade_mode,
            limit_orders=mt_obj.limit_orders,
            margin=mt_obj.margin,
            margin_free=mt_obj.margin_free,
            margin_level=mt_obj.margin_level,
            equity=mt_obj.equity,
            balance=mt_obj.balance,
            profit=mt_obj.profit,
            credit=mt_obj.credit,
            name=mt_obj.name,
            server=mt_obj.server,
            currency=mt_obj.currency,
            company=mt_obj.company,
        )


class MTTerminal(Base):
    build: int = None
    #community_account: int = None
    #community_connection: int = None
    connected: int = None
    trade_allowed: int = None
    ping_last: int = None
    #retransmission: float = None
    #language: str = None
    name: str = None
    company: str = None
    path: str = None
    data_path: str = None
    commondata_path: str = None

    @classmethod
    def from_mt_obj(cls, mt_obj):
        return cls(
            build=mt_obj.build,
            connected=mt_obj.connected,
            trade_allowed=mt_obj.trade_allowed,
            ping_last=mt_obj.ping_last,
            name=mt_obj.name,
            company=mt_obj.company,
            path=mt_obj.path,
            data_path=mt_obj.data_path,
            commondata_path=mt_obj.commondata_path
        )

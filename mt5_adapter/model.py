
from typing import Tuple
import pydantic
import datetime
from mt5_adapter.log import my_logger


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

    def map_attributes_from_mt_object(self, mt_object: Tuple):
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
    volume_step: float = None
    category: str = None
    name: str = None




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


class MTDeal(Base):
    magic: int = None
    state: int = None
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
    sl: float = None
    tp: float = None
    symbol: str = None
    comment: str = None



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


class MTTerminal(Base):
    build: int = None
    community_account: int = None
    community_connection: int = None
    connected: int = None
    trade_allowed: int = None
    ping_last: int = None
    retransmission: float = None
    language: str = None
    name: str = None
    company: str = None
    path: str = None
    data_path: str = None
    commondata_path: str = None

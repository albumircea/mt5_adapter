import asyncio
import concurrent.futures
import MetaTrader5 as _mt5
from terminal.utils import *
from terminal.wrappers import timing

class MTClient:

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_running_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor()

    async def initialize(self, path: str = None, login: str = None, password: str = None, server: str = None, portable: bool = False, timeout: int = None,) -> bool:
        args = reduce_args(locals().copy())
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.initialize(**args))

    async def shutdown(self) -> None:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.shutdown())

    async def last_error(self):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.last_error())

    async def account_info(self):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.account_info())

    async def terminal_info(self):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.terminal_info())

    async def symbols_total(self) -> int:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.symbols_total())

    async def symbols_get(self, group: str = None):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.symbols_get(group=group))

    async def symbol_info(self, symbol: str):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.symbol_info(symbol))

    async def symbol_info_tick(self, symbol: str):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.symbol_info_tick(symbol))

    async def symbol_select(self, symbol: str, enable: bool = True) -> bool:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.symbol_select(symbol, enable))

    async def orders_total(self) -> int:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.orders_total())

    async def order_calc_margin(self, order_type: int, symbol: str, volume: float, price: float,) -> float:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.order_calc_margin(order_type, symbol, volume, price))

    async def order_check(self, request: dict):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.order_check(request))

    async def order_send(self, request):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.order_send(request))

    async def positions_total(self) -> int:
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.positions_total())

    async def positions_get(self, symbol: str = None, group: str = None):
        """Get open positions with the ability to filter by symbol or ticket. There are three call options."""
        dict = locals().copy()
        kw = reduce_args_by_keys(dict, ['symbol', 'group'])
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.positions_get(**kw))

    async def position_get_by_ticket(self, ticket: int):
        return await self.loop.run_in_executor(self.executor, lambda: _mt5.positions_get(ticket=ticket))

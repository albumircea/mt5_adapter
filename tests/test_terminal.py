from mt5_adapter import __version__

from mt5_adapter.config import main_terminal_path, terminal_paths

from mt5_adapter.client import MTClient

from mt5_adapter.trade import *
import asyncio

from mt5_adapter.wrappers import timing


terminal_workers: MTClient = []

symbol = "EURUSD"


async def spawn_terminals():

    for _ in range(len(terminal_paths)):
        terminal_workers.append(MTClient())

    index = 0
    for terminal in terminal_workers:
        await terminal.initialize(terminal_paths[index])
        index += 1

    main_terminal = MTClient()
    terminal_workers.insert(0, main_terminal)

    await main_terminal.initialize()


async def test_buy(client: MTClient):

    await open_buy(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=11)


async def test_sell(client: MTClient):

    await open_sell(metatrader=client, symbol_name=symbol, volume=0.01, magic_number=22)


async def open_n_fast(client: MTClient, n):

    buys = [test_buy(client) for _ in range(n)]

    sells = [test_sell(client) for _ in range(n)]

    await asyncio.gather(*buys, *sells)


async def close_all_fast(client: MTClient):

    positions = await positions_get_all(metatrader=client, symbol=symbol)

    closed = [position_close(metatrader=client, ticket=position.ticket) for position in positions]

    await asyncio.gather(*closed)


@timing
async def madness():

    n = 10

    # info = await terminal_list[2].account_info()

    # my_logger.info(f"info = {info}")
    return
    task1 = [test_buy(terminal_workers[0]) for _ in range(n)]

    task2 = [test_buy(terminal_workers[1]) for _ in range(n)]

    task3 = [test_buy(terminal_workers[2]) for _ in range(n)]

    task4 = [test_buy(terminal_workers[3]) for _ in range(n)]

    task5 = [test_buy(terminal_workers[4]) for _ in range(n)]

    await asyncio.gather(*task1, *task2, *task3, *task4, *task5)


async def run_tests():
    await spawn_terminals()

    await madness()


if __name__ == "__main__":

    asyncio.run(run_tests())

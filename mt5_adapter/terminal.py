from typing import Tuple, Union
from mt5_adapter.client import MTClient
from mt5_adapter.model import MTTerminal


async def initialize(metatrader:MTClient,path: str = None, login: str = None, password: str = None, server: str = None, portable: bool = False, timeout: int = None,) -> bool:
    initialized = await metatrader.initialize(path=path,login=login,password=password,server=server,portable=portable,timeout=timeout)
    return initialized

async def shutdown(metatrader:MTClient)->bool:
    shut_down = await metatrader.shutdown()
    return shut_down


async def get_terminal_info_raw(metatrader:MTClient):
    return await metatrader.terminal_info()


async def get_terminal_info(metatrader:MTClient)->Union[MTTerminal, None]:
    info = await metatrader.terminal_info()
    if info:
        terminal_info = MTTerminal()
        terminal_info.from_mt_object(info)
        return terminal_info
    return None


async def get_terminal_version(metatrader:MTClient)->Tuple[int,int,int]:
    version  = await metatrader.version()
    return version

async def get_last_error(metatrader:MTClient) ->Tuple[int,str]:
    last_error = await metatrader.last_error()
    return last_error


from typing import Union
from mt5_adapter.client import MTClient
from mt5_adapter.model import MTAccount


async def login(metatrader:MTClient,login:int,password:str,server:str=None,timeout:int=None)->bool:
    logged = await metatrader.login(login=login,password=password,server=server,timeout=timeout)
    return logged


async def get_account_info_raw(metatrader:MTClient):
    return await metatrader.account_info()


async def get_account_info(metatrader:MTClient) -> Union[MTAccount, None]:
    info = await metatrader.account_info()
    if info:
        account_info = MTAccount()
        account_info.map_attributes_from_mt_object(info)
        return account_info
    return None
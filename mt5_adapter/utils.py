from datetime import datetime
from .log import my_logger
from typing import Any, Iterable




def args_to_str(args: tuple, kwargs: dict):
    ar = ', '.join(map(str, args))
    kw = ', '.join(f"{k}={v}" for k, v in kwargs.items())
    return ar + (', ' if ar and kw else '') + kw


def __ify(data, apply_methods):
    for method in apply_methods:
        if hasattr(data, method):  # noqa
            #my_logger.error(f"data: {data}    method : {method}")
            return __ify(getattr(data, method)(), apply_methods)  # noqa
    T = type(data)

    if T is tuple or T is list:
        #res = T(__ify(i, apply_methods) for i in data)
        return T(__ify(i, apply_methods) for i in data)

    if T is dict:
        # res = {k: __ify(v, apply_methods) for k, v in data.items()}
        #my_logger.debug(f"dict res: {res}")
        return {k: __ify(v, apply_methods) for k, v in data.items()}

    return data


def dictify(data: Any):
    """Convert all nested data returns to native python (pickleable) data structures. Example: List[OrderSendResult]
    -> List[dict]

    :param data: Any API returned result from the MetaTrader5 API
    :return:
    """
    # if hasattr(data, '_asdict'):  # noqa
    #     return dictify(data._asdict()) # noqa
    # T = type(data)
    # if T is tuple or T is list:
    #     return T(dictify(i) for i in data)
    # if T is dict:
    #     return {k: dictify(v) for k, v in data.items()}
    return __ify(data, ['_asdict'])


def is_rates_array(array):
    try:
        rate = array[0]
        return type(rate) is tuple and len(rate) == 8
    except Exception as e:
        return False


def reduce_args(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None and k != 'kwargs'}


def reduce_args_by_keys(d: dict, keys: Iterable) -> dict:
    return {k: v for k, v in d.items() if k in keys and v is not None}


def reduce_combine(d1: dict, d2: dict):
    d1 = reduce_args(d1)
    for k, v in d2.items():
        if v is not None:
            d1[k] = v
    return d1


def chunks(_list, chunk_size):
    chunk_size = max(1, chunk_size)
    return [_list[i:i + chunk_size] for i in range(0, len(_list), chunk_size)]
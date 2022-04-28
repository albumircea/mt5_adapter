



from functools import wraps
from timeit import default_timer as timer
from mt5_adapter.log import my_logger

def timing(coro):
    @wraps(coro)
    async def wrapper(*args,**kwargs):
        start = timer()
        result = await coro(*args,**kwargs)
        end = timer()
        my_logger.info(f" {coro.__name__} took {end - start:.5} seconds to run")
        return result
    return wrapper

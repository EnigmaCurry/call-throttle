import asyncio
import threading
from functools import wraps

from .throttle import Throttle, AsyncThrottle


def throttle(calls, period, raise_on_throttle=False):
    """A throttle decorator factory used to limit function or asyncio coroutine
    calls during the defined time period.

    Args:
        calls (int): The maximum number of function calls within a time period
            before throttling.
        period (datetime.timedelta): A time period within which the throttling
            applies to function calls.
        raise_on_throttle (bool): A flag indicating whether to raise an
            exception when throttling.

    Returns:
        A decorator suited for functions and asyncio coroutines.

    Raises:
        ThrottleException (when raise_on_throttle is True and throttle occurs)

    Usage:
        >>> import datetime
        >>> from call_throttle import throttle
        >>> @throttle(calls=1, period=datetime.timedelata(seconds=1))
        >>> def func():
        ...     pass
        >>> @throttle(calls=10, period=datetime.timedelata(milliseconds=100))
        >>> async def coro():
        ...     pass
    """

    def decorator(func):

        if asyncio.iscoroutinefunction(func):
            thr = AsyncThrottle(calls, period, raise_on_throttle)
            lock = asyncio.Lock()

            @wraps(func)
            async def wrapper(*args, **kwargs):

                async with lock:
                    await thr.call()

                return await func(*args, **kwargs)

        else:
            thr = Throttle(calls, period, raise_on_throttle)
            lock = threading.RLock()

            @wraps(func)
            def wrapper(*args, **kwargs):

                with lock:
                    thr.call()

                return func(*args, **kwargs)

        return wrapper

    return decorator

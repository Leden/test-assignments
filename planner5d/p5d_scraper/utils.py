import asyncio
import typing as t


async def arange(*args: int) -> t.AsyncGenerator[int, None]:
    # this should be part of standard library, but apparently is not?..
    for i in range(*args):
        yield i
        await asyncio.sleep(0)

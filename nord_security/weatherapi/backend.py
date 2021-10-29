from aiohttp import ClientSession
from furl import furl

from . import config


async def query_weather(query):
    url = furl(config.OWM_ENDPOINT)
    url.args["appid"] = config.OWM_API_KEY
    url.args["q"] = query

    async with ClientSession() as session:
        async with session.get(str(url)) as response:
            return await response.text()

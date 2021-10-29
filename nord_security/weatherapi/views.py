from aiohttp import web

from .backend import query_weather
from .token import create_token


async def get_weather(request):
    query = request.query.get("q")
    if not query:
        return web.HTTPBadRequest(reason='Missing query parameter: "q".')

    text = await query_weather(query)
    return web.Response(text=text, content_type="application/json")


async def get_token(request):
    token = create_token()
    return web.Response(text=token)

from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from . import config
from .views import get_token, get_weather

app = web.Application(
    middlewares=[
        JWTMiddleware(
            config.JWT_SECRET,
            whitelist=("/token",),
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUDIENCE,
            issuer=config.JWT_ISSUER,
        ),
    ]
)
app.router.add_get("/weather", get_weather)
app.router.add_get("/token", get_token)

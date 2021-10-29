"""
App configuration reading from environment variables.
Raising when a required variable is missing.
Casting configuration variables to the correct types.
"""

import os
from datetime import timedelta

from .exceptions import ConfigError

# API endpoint to call
OWM_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

# OWM API key. Required.
OWM_API_KEY = os.environ["OWM_API_KEY"]
if not OWM_API_KEY:
    raise ConfigError("OWM_API_KEY is missing from the environment.")

# JWT parameters.
# NB: Changing any of SECRET, AUDIENCE, ISSUER, ALGORITHM variables
# will invalidate all previousl issued tokens.

# JWT secret used to sign tokens. Required.
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise ConfigError("JWT_SECRET is missing from the environment.")

# JWT audience. Can be empty.
JWT_AUDIENCE = os.environ.get("JWT_AUDIENCE")

# JWT issuer. Can be empty.
JWT_ISSUER = os.environ.get("JWT_ISSUER")

# JWT algorithm. If not given, will use HS256 as default.
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

# JWT expiration in seconds. If not given, tokens will expire instantly.
JWT_EXPIRATION = timedelta(seconds=int(os.environ.get("JWT_EXPIRATION", 0)))

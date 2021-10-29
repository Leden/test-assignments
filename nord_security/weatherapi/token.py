from datetime import datetime

import jwt

from . import config


def create_token():
    expiration = datetime.utcnow() + config.JWT_EXPIRATION
    payload = {"aud": config.JWT_AUDIENCE, "iss": config.JWT_ISSUER, "exp": expiration}
    return jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)

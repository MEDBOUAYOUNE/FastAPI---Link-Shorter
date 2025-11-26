import jwt
import datetime

from app.settings import JWT_SECRET, JWT_ALGORITHM
from .responses import success_response, error_response

# generate JWT tokens
# Verify JWT tokens
# Refresh Access Token based on Refresh Token
# Blacklist tokens (optional)



def create_jwt_tokens(user_id: int) -> tuple[str, str]:
    """ """
    access_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    refresh_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    payload_access = {
        "user_id": str(user_id),
        "exp": access_expiry,
        "type": "access"
    }

    payload_refresh = {
        "user_id": str(user_id),
        "exp": refresh_expiry,
        "type": "refresh"
    }

    access_token = jwt.encode(payload_access, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(payload_refresh, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return access_token, refresh_token

def decode_jwt_token(token: str) -> dict:
    """ """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    

def verify_token(token: str, token_type: str) -> dict:
    """ """
    payload = decode_jwt_token(token)

    if not payload or "type" not in payload and payload["type"] != token_type:
        raise ValueError("Invalid token type")
    return payload


def refresh_access_token(refresh_token: str) -> str:
    """ """
    payload = verify_token(refresh_token, token_type="refresh")
    user_id = payload["user_id"]

    new_access_token, _ = create_jwt_tokens(user_id=user_id)
    return new_access_token
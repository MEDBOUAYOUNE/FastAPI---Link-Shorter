# import jwt
# import datetime

# from app.settings import JWT_SECRET, JWT_ALGORITHM


# def create_jwt_tokens(user_id: int) -> tuple[str, str]:
#     """ """
#     access_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
#     refresh_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)

#     payload_access = {
#         "user_id": str(user_id),
#         "exp": access_expiry,
#         "type": "access"
#     }

#     payload_refresh = {
#         "user_id": str(user_id),
#         "exp": refresh_expiry,
#         "type": "refresh"
#     }

#     access_token = jwt.encode(payload_access, JWT_SECRET, algorithm=JWT_ALGORITHM)
#     refresh_token = jwt.encode(payload_refresh, JWT_SECRET, algorithm=JWT_ALGORITHM)

#     return access_token, refresh_token

# def decode_jwt_token(token: str) -> dict:
#     """ """
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         return {"error": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"error": "Invalid token"}
    

# def verify_token(token: str, token_type: str) -> bool:
#     """ """
#     payload = decode_jwt_token(token)
#     if "error" in payload:
#         return False
#     return payload.get("type") == token_type


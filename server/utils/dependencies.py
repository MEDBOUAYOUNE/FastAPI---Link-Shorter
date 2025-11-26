from fastapi import Depends, HTTPException, Request
from app.db import Session, get_db
from utils.jwt import verify_token

async def is_authenticated_user(request: Request) -> str:
    """ """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token, token_type="access")
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return user_id
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
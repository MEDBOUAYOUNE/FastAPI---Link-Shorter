from fastapi import Depends, HTTPException, Request
from app.db import Session, get_db
from utils.jwt import verify_token
from models.user import User

async def is_authenticated_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user from JWT token"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        token = auth_header.split(" ")[1]
        payload = verify_token(token, token_type="access")
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # Fetch user from database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
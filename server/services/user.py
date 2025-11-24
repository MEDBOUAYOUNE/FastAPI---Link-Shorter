
from schemas.user import UserCreate
from app.db import Base, Session
from models.user import User



async def create_user(user: UserCreate, db: Session):
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=User.__hashed_password__(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}
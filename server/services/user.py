
from schemas.user import UserCreate, UserLogin
from app.db import Base, Session
from models.user import User



async def create_user(user: UserCreate, db: Session):
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=User.encode_password(password=user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}


async def login(user: UserLogin, db: Session):
    _user = db.query(User).filter(User.email == user.email).first()
    if not _user:
        return {"error": "Invalid email or password"}
    if not _user.verify_password(user.password):
        return {"error": "Invalid email or password"}
    return {"message": "Login successful", "user_id": _user.id}



from sqlalchemy.exc import IntegrityError

from app.db import Session
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.responses import success_response, error_response



async def create_user(user: UserCreate, db: Session):
    try:
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=User.encode_password(password=user.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return success_response(
            status="success",
            data={"user_id": new_user.id},
            message="User created successfully",
            status_code=201
            )
    except IntegrityError:
        db.rollback()
        return error_response(
            status="error",
            message="Email already registered",
            status_code=400
        )  


async def login(user: UserLogin, db: Session):
    _user = db.query(User).filter(User.email == user.email).first()
    if not _user:
        return error_response(
            status="error",
            message="Invalid email or password",
            code=401
        )
    if not _user.verify_password(user.password):
        return error_response(
            status="error",
            message="Invalid email or password",
            code=401
        )
    return success_response(
        status="success",
        data={"user_id": _user.id},
        message="Login successful",
        status_code=200
    )


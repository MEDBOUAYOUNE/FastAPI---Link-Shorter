
from sqlalchemy.exc import IntegrityError
from fastapi import Request
from app.db import Session
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.responses import success_response, error_response
from utils.jwt import create_jwt_tokens, refresh_access_token



async def register_service(user: UserCreate, db: Session):
    try:
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=User.encode_password(password=user.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token, refresh_token = create_jwt_tokens(user_id=new_user.id)
        response = success_response(
            status="success",
            data={"user_id": str(new_user.id),
                  "access_token": str(access_token)},
            message="User created successfully",
            status_code=201
            )
        response.set_cookie(key="refresh_token",
                            value=str(refresh_token),
                            httponly=True
                            )
        return response
    except IntegrityError:
        db.rollback()
        return error_response(
            status="error",
            message="Email already registered",
            status_code=400
        )
    except Exception as e:
        db.rollback()
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )


async def login_service(user: UserLogin, db: Session):
    try:
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
        access_token, refresh_token = create_jwt_tokens(user_id=_user.id)
        response =  success_response(
            status="success",
            data={"user_id": str(_user.id),
                  "access_token": str(access_token)
                  },
            message="Login successful",
            status_code=200
        )
        response.set_cookie(key="refresh_token",
                            value=str(refresh_token),
                            httponly=True
                )
        return response
    except Exception as e:
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )

async def refresh_token_service(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        new_access_token = refresh_access_token(refresh_token)
        return success_response(
            status="success",
            data={"access_token": str(new_access_token)},
            message="Access token refreshed successfully",
            status_code=200
        )
    except ValueError as e:
        return error_response(
            status="error",
            message=str(e),
            status_code=401
        )


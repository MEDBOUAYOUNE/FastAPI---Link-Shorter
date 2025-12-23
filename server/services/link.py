from fastapi import Depends, Request
from app.db import Session, get_db
from app.settings import BASE_URL
from models.link import Link
from models.user import User
from utils.responses import success_response, error_response
from utils.dependencies import is_authenticated_user


async def create_link_service(original_url: str, user: User = Depends(is_authenticated_user), db: Session = Depends(get_db)):
    try:
        # Generate short code
        short_code = Link.generate_shortened_url(BASE_URL).split('/')[-1]
        
        new_link = Link(
            original_url=original_url,
            shortened_url=short_code,
            user_id=user.id
        )
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
        
        short_url = f"{BASE_URL}/link/{new_link.shortened_url}"
        
        return success_response(
            status="success",
            data={
                "link_id": str(new_link.id),
                "short_code": new_link.shortened_url,
                "short_url": short_url,
                "original_url": new_link.original_url
            },
            message="Link created successfully",
            status_code=201
        )
    except Exception as e:
        db.rollback()
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )

async def get_link_service(link_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.id == link_id).first()
        if not link:
            return error_response(
                status="error",
                message="Link not found",
                status_code=404
            )
        link.increment_open_count(request.client.host)
        db.commit()
        db.refresh(link)
        return success_response(
            status="success",
            data={"link": {
                "id": link.id,
                "original_url": link.original_url,
                "shortened_url": link.shortened_url,
            }},
            message="Link fetched successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )

async def get_link_by_short_code_service(short_code: str, request: Request, db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.shortened_url == short_code).first()
        if not link:
            return error_response(
                status="error",
                message="Link not found",
                status_code=404
            )
        
        if request.client:
            link.increment_open_count(request.client.host)
            db.commit()
        
        return success_response(
            status="success",
            data={
                "original_url": link.original_url,
                "short_code": link.shortened_url
            },
            message="Link found",
            status_code=200
        )
    except Exception as e:
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )

async def delete_link_service(short_code: str, user: User = Depends(is_authenticated_user), db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.shortened_url == short_code, Link.user_id == user.id).first()
        if not link:
            return error_response(
                status="error",
                message="Link not found or unauthorized",
                status_code=404
            )
        db.delete(link)
        db.commit()
        return success_response(
            status="success",
            message="Link deleted successfully",
            status_code=200
        )
    except Exception as e:
        db.rollback()
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )

async def get_link_stats_service(short_code: str, user: User = Depends(is_authenticated_user), db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.shortened_url == short_code, Link.user_id == user.id).first()
        if not link:
            return error_response(
                status="error",
                message="Link not found or unauthorized",
                status_code=404
            )
        stats = {
            "open_count": link.open_count,
            "open_ips": link.open_ips,
            "created_at": link.created_at.isoformat()
        }
        return success_response(
            status="success",
            data={"stats": stats},
            message="Link statistics fetched successfully",
            status_code=200
        )
    except Exception as e:
        return error_response(
            status="error",
            message=str(e),
            status_code=500
        )
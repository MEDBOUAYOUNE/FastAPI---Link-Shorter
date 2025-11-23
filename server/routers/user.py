from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/")
def read_users():
    return {"message": "Test user endpoint"}
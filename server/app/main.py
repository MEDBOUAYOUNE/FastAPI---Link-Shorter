from fastapi import FastAPI

from app.db import Base, engine
from routers import user
from utils.redis import init_redis



app = FastAPI()

redis_client = init_redis()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)


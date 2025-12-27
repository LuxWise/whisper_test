from fastapi import APIRouter
from app.core.database import Base, engine
from app.api.v1.endpoints import users
from app.api.v1.endpoints import transcribe

Base.metadata.create_all(bind=engine)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transcribe.router, prefix="/transcribe", tags=["transcribe"])
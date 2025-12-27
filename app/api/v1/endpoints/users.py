from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return user_service.get_users_service(db=db)

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user_service(db=db, user=user)
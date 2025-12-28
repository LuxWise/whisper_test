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

@router.get("/users/{user_email}", response_model=UserResponse)
async def get_user(user_email: str, db: Session = Depends(get_db)):
    return user_service.get_user_service(db=db, user_email=user_email)
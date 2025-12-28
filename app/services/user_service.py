from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.schema.user import UserCreate

def create_user_service(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        hashed_password=hashed_password  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_service(db: Session):
    return db.query(User).all()

def get_user_service_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()
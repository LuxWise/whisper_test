from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
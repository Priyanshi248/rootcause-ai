from pydantic import BaseModel, EmailStr

from uuid import UUID

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str




class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
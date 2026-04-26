from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    account_type: str = 'cliente'
    terms_accepted: str = 'Y'
    is_active: str = 'Y'

class UserCreate(UserBase):
    password: str  #Senha em texto plano

class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name : str
    email : EmailStr
    password : str

    class config:
        orm_mode = True # it will convert sqlalchemy into pydantic model

class UserCreate(UserBase):
    inst_id : int
    is_master : Optional[bool]

    class Config:
        orm_mode = True 

class UserOut(BaseModel):
    id : int
    name : str
    email : EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    role : str

    class Config:
        orm_mode = True

class UserPassUpdate(BaseModel):
    old_password : str
    new_password : str

    class Config:
        orm_mode = True
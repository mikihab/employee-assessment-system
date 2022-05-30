from typing import Optional
from pydantic import BaseModel

class InstCreate(BaseModel):
    name : str
    city : str
    state : str
    country : str

    class Config:
        orm_mode = True

class InstOut(BaseModel):
    name : str
    city : str
    state : str
    country : str

    class Config:
        orm_mode = True

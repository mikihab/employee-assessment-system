from pydantic import BaseModel

class DeptCreate(BaseModel):
    dept_code : str
    dept_name : str
    user_id : int

    class Config:
        orm_mode = True

class DeptUpdate(BaseModel):
    dept_name : str
    
    class Config:
        orm_mode = True
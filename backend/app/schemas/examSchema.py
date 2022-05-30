from typing import Optional
from pydantic import BaseModel

#Exam
class ExamCreate(BaseModel):
    dept_id : int
    title : str
    description : Optional[str]

    class Config:
        orm_mode = True

class ExamStatus(BaseModel):
    exam_active : bool

class ExamOut(ExamCreate):
    exam_active : bool

class ExamAssign(BaseModel):
    user_id : int
    exam_id : int
    exam_status : Optional[str]

#Exam Question
class AddQstn(BaseModel):
    exam_id : int
    question : str
    ch1 : str
    ch2 : str
    ch3 : str
    ch4 : str
    answer : str
    status : Optional[bool]

    class Config:
        orm_mode = True

class QstnOut(BaseModel):
    exam_id : int
    question : str
    ch1 : str
    ch2 : str
    ch3 : str
    ch4 : str

    class Config:
        orm_mode = True

#Exam Answer
class UserExam(BaseModel):
    exam_id : int
    user_id : int

    class Config:
        orm_mode = True

class UserAns(UserExam):
    qstn_id : int
    user_answer : str

    class Config:
        orm_mode = True

from typing import List
from .. import models, oauth2
from ..schemas import examSchema
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/answer",
    tags=["Exam-Answer"]
)

@router.post("/")
def add_answer(ans : examSchema.UserAns, db: Session = Depends(get_db),token : int= Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
     detail="not authorized to perform the request")
   
    if token.role != 'student':
        raise credential_exception
    if int(token.id) != ans.user_id:
        raise credential_exception

    query = db.query(models.ExamAtmpt).filter(models.ExamAtmpt.exam_id == ans.exam_id , models.ExamAtmpt.user_id == ans.user_id)
    if query.first() == None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail="exam not found")

    query = db.query(models.ExamAns).filter(models.ExamAns.exam_id == ans.exam_id,
     models.ExamAns.qstn_id == ans.qstn_id, models.ExamAns.user_id == ans.user_id)

    if query.first() == None:
        answer = models.ExamAns(**ans.dict())
    
        db.add(answer)
        db.commit()
        db.refresh(answer)
    else:
        query.update(ans.dict(), synchronize_session=False)
        db.commit()

    return query.first()

@router.get("/",response_model= List[examSchema.UserAns])
def get_student_answer(user: examSchema.UserExam,db: Session = Depends(get_db),token : int= Depends(oauth2.get_current_user)):
    query = db.query(models.Exam).join(models.Department,
     models.Exam.id == models.Department.id).join(models.User,
     models.User.id == models.Department.user_id).filter(models.User.id == token.id)
    
    if token.role != "teacher" or query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the request")   


    stdnt_query = db.query(models.User).filter(models.User.id == user.user_id)
    exam_query = db.query(models.Exam).filter(models.Exam.id == user.exam_id)

    if stdnt_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"student with id {user.user_id} not found")

    elif exam_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"exam with id {user.exam_id} not found")

    query = db.query(models.ExamAns).filter(models.ExamAns.exam_id == user.exam_id,models.ExamAns.user_id == user.user_id)
 
    return query.all()

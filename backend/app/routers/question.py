from typing import Optional, List
from .. import models, oauth2
from ..schemas import examSchema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/question",
    tags=["Exam-Question"]
)

@router.post("/",response_model=examSchema.QstnOut)
def add_exam_question(qstn : examSchema.AddQstn ,db: Session = Depends(get_db),token : int= Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the request")

    if token.role != "master":
        raise credential_exception

    query = db.query(models.User).join(models.Department,
     models.User.id == models.Department.user_id).join(models.Exam,
     models.Department.id == models.Exam.dept_id).filter(models.User.id == token.id)
    
    if query.first() == None:
        raise credential_exception
    
    new_qstn = models.ExamQstn(**qstn.dict())
    db.add(new_qstn)
    db.commit()
    db.refresh(new_qstn)

    return new_qstn


@router.get("/",response_model=List[examSchema.QstnOut])
def get_exam_question(examId : int, db: Session = Depends(get_db),token: int= Depends(oauth2.get_current_user)):
    query = db.query(models.ExamQstn).join(models.Exam,
     models.ExamQstn.exam_id == models.Exam.id).join(models.Department,models.Exam.dept_id==models.Department.id).filter(models.Exam.id == examId,
     models.Department.user_id==token.id)

    return query.all()


@router.delete("/{id}")
def delete_exam_question(id: int,db: Session = Depends(get_db),token: int= Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the request")

    if token.role != "master":
        raise credential_exception

    query = db.query(models.User).join(models.Department,
     models.User.id == models.Department.user_id).join(models.Exam,
     models.Department.id == models.Exam.dept_id).join(models.ExamQstn,
     models.Exam.id == models.ExamQstn.exam_id).filter(models.User.id == token.id,
     models.ExamQstn.id == id)

    print(query)
    if query.first() == None:
        raise credential_exception
    query = db.query(models.ExamQstn).filter(models.ExamQstn.id == id)
    qstn = query.first()
    if not qstn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"question with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"deleted question with id {id}"}
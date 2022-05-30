from .. import models, oauth2
from ..schemas import examSchema
from fastapi import Query, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/exam",
    tags=["Exam"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=examSchema.ExamOut)
def add_exam(exam: examSchema.ExamCreate, db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "master":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    #checking if logged in teacher is the creator of department which exam is to be created under 
    query = db.query(models.User).join(models.Department,models.User.id == models.Department.user_id).filter(models.Department.id == exam.dept_id,models.User.id == token.id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")
    new_exam = models.Exam(**exam.dict())
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return new_exam


@router.put("/",response_model=examSchema.ExamOut)
def exam_status_change(id :int, exam_status :examSchema.ExamStatus,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "master":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    #checking if logged in teacher is the creator of the department or exam
    query = db.query(models.User).join(models.Department,models.User.id == models.Department.user_id).join(models.Exam,
     models.Department.id == models.Exam.dept_id).filter(models.User.id == token.id, models.Exam.id == id)

    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")     
    
    query = db.query(models.Exam).filter(models.Exam.id==id)
    exam = query.first()
    if exam == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exam with {id} doesnt exist")

    if exam_status.exam_active == True:
        if exam.exam_active == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"exam is already active")
        query.update(exam_status.dict(), synchronize_session=False)
        db.commit()
    else:
        if exam.exam_active == False:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"exam is already not active")
        query.update(exam_status.dict(), synchronize_session=False)
        db.commit()

    return query.first()


@router.delete("/{id}")
def delete_exam(id: int,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "master":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    #checking if logged in teacher is the creator of department / exam 
    query = db.query(models.User).join(models.Department,models.User.id == models.Department.user_id).join(models.Exam,
     models.Department.id == models.Exam.dept_id).filter(models.User.id == token.id, models.Exam.id == id)

    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action") 

    query = db.query(models.Exam).filter(models.Exam.id == id)
    exam = query.first()
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"exam with id {id} not found")
    if exam.exam_active == True:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"can't delete active exam")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"deleted exam with id {id}"}


@router.post("/assign-student")
def assign_users_to_exam(assign : examSchema.ExamAssign,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "master":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")
    
    #checking if logged in user is creator of department / exam
    query = db.query(models.User).join(models.Department,models.User.id == models.Department.user_id).join(models.Exam,
     models.Department.id == models.Exam.dept_id).filter(models.User.id == token.id, models.Exam.id == assign.exam_id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")   

    #checking if employee is in the same institution as the user who created the exam   
    query = db.query(models.User).join(models.User, models.User.inst_id == models.User.inst_id).join(models.Department,
     models.User.id == models.Department.user_id).filter(models.User.id == assign.user_id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")   


    stdnt_query = db.query(models.User).filter(models.User.id == assign.user_id)
    exam_query = db.query(models.Exam).filter(models.Exam.id == assign.exam_id)
    
    if stdnt_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with id {assign.user_id} not found")
    elif exam_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"exam with id {assign.exam_id} not found")
    
    assignTo = models.ExamAtmpt(**assign.dict())
    db.add(assignTo)
    db.commit()
    db.refresh(assignTo)

    return assignTo


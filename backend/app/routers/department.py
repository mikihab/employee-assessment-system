from .. import models, oauth2
from ..schemas import deptSchema
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/department",
    tags=["Department"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=deptSchema.DeptCreate)
def add_dept(dept: deptSchema.DeptCreate, db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    if token.role != "master" or dept.user_id != int(token.id):
        raise credential_exception

    new_course = models.Department(**dept.dict())
    try:
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
         detail=f"department with code {dept.dept_code} already exists")

    return new_course

@router.get("/",response_model=List[deptSchema.DeptCreate])
def get_depts(db: Session = Depends(get_db),limit: int = 10,search: Optional[str] = ""):
  
    courses = db.query(models.Department).filter(models.Department.dept_name.contains(search)).limit(limit).all()

    return courses

@router.get("/{id}",response_model=deptSchema.DeptCreate)
def get_dept(id: int,db: Session = Depends(get_db)):
    course = db.query(models.Department).filter(models.Department.id == id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"department with id {id} not found")

    return course

@router.put("/{id}",response_model=deptSchema.DeptCreate)
def update_dept(id: int,user: deptSchema.DeptUpdate,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    if token.role != "master":
        raise credential_exception

    #checking if logged in teacher is the creator of the course to be updated
    query = db.query(models.Department).filter(models.Department.user_id == token.id, models.Department.id == id)
    
    if query.first() == None:
        credential_exception

    query = db.query(models.Department).filter(models.Department.id==id)

    to_be_updated = query.first()

    if to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"department with {id} doesnt exist")

    query.update(user.dict(), synchronize_session=False)
    db.commit()
    
    return query.first()


@router.delete("/{id}")
def delete_dept(id: int,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    if token.role != "master":
        raise credential_exception

    #checking if logged in teacher is the creator of the course to be deleted
    query = db.query(models.User).filter(models.Department.user_id == token.id, models.Department.id == id)
    
    if query.first() == None:
        raise credential_exception

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"department with id {id} not found")
    
    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"deleted department with id {id}"}
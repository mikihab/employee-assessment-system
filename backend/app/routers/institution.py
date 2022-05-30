from .. import models, oauth2
from ..schemas import instSchema 
from typing import Optional, List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/institution",
    tags=['Institution']
)

#Adding institution
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=instSchema.InstOut)
def add_institution(inst: instSchema.InstCreate, db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    new_inst = models.Institution(**inst.dict())
    db.add(new_inst)
    db.commit()
    db.refresh(new_inst)

    return new_inst

@router.get("/",response_model=List[instSchema.InstOut])
def get_institutions(db: Session = Depends(get_db),limit: int = 10,search: Optional[str] = ""):
  
    insts = db.query(models.Institution).filter(models.Institution.name.contains(search)).limit(limit).all()

    return insts

@router.get("/{id}",response_model=instSchema.InstOut)
def get_institution(id: int,db: Session = Depends(get_db)):
    inst = db.query(models.Institution).filter(models.Institution.id == id).first()

    if not inst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"institution with id {id} not found")

    return inst

@router.put("/{id}",response_model=instSchema.InstOut)
def update_institution(id: int,inst: instSchema.InstCreate,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    query = db.query(models.Institution).filter(models.Institution.id==id)

    to_be_updated = query.first()

    if to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"institution with {id} doesnt exist")

    query.update(inst.dict(), synchronize_session=False)
    db.commit()
    
    return query.first()


@router.delete("/{id}")
def delete_institution(id: int,db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    if token.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    query = db.query(models.Institution).filter(models.Institution.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"institution with id {id} not found")
    
    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"deleted institution with id {id}"}
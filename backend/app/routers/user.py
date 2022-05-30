from .. import models, utils, oauth2
from ..schemas import userSchema
from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=userSchema.UserOut)
def register_user(user: userSchema.UserCreate, db: Session = Depends(get_db)):
    query = db.query(models.Institution).filter(models.Institution.id == user.inst_id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"institution with id {user.inst_id} not found")

    #hashing password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/",response_model=List[userSchema.UserOut])
async def get_users(db: Session = Depends(get_db),limit: int = 10,search: Optional[str] = ""):
  
    users = db.query(models.User).filter(models.User.name.contains(search)).limit(limit).all()
    print(users)
    return users


@router.get("/{id}",response_model=userSchema.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with id {id} not found")

    return user    


@router.delete("/{id}")
def delete_user(id: int,db: Session = Depends(get_db),token: int =Depends(oauth2.get_current_user)):
    if token.role!='user' or int(token.id) != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not authorized to perform the requested action")

    query = db.query(models.User).filter(models.User.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with id {id} not found")
    
    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"deleted user with id {id}"}
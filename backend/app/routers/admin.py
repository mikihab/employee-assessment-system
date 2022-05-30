from .. import models, utils, oauth2
from ..schemas  import userSchema, tokenSchema
from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)
#Login admin
@router.post("/login",response_model=tokenSchema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db :Session = Depends(get_db)):
    
    #OAuth2PasswordRequestForm stores email as username
    user = db.query(models.Admin).filter(models.Admin.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    #create token
    access_token = oauth2.create_access_token(data = {"role": 'admin',"user_id": user.id})

    return {'access_token': access_token, "token_type": "bearer"}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=userSchema.UserOut)
def create_admin(admin: userSchema.UserBase, db: Session = Depends(get_db)):

    #hashing password
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password

    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin
    
@router.put("/", response_model=userSchema.UserOut)
def change_password(credential: userSchema.UserPassUpdate, db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):

    if token.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    query = db.query(models.Admin).filter(models.Admin.id == token.id)
    user = query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail="unable to find details")
    
    if int(token.id) != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform requested action")
    else:
        if not utils.verify(credential.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
             detail="Invalid Credentials")
    
    password = utils.hash(credential.new_password)
    
    query.update({'password': password},synchronize_session=False)
    db.commit()

    return query.first()


  


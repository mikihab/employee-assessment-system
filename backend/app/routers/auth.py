from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2
from ..schemas import tokenSchema, userSchema


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login',response_model=tokenSchema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db :Session = Depends(get_db)):
#OAuth2PasswordRequestForm stores email as username

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if user.is_master == False:
        usertype = 'user'
    elif user.is_master == True:
        usertype = 'master'    
    #create token
    access_token = oauth2.create_access_token(data = {"role":usertype,"user_id": user.id})
   
    return {'access_token': access_token, "token_type": "bearer", 'user': usertype}

@router.put("/change-password", response_model=userSchema.UserOut)
def change_password(credential: userSchema.UserPassUpdate, db: Session = Depends(get_db),token: int = Depends(oauth2.get_current_user)):
    
    if token.role != 'user':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
         detail="not authorized to perform the requested action")

    query = db.query(models.User).filter(models.User.id == token.id)    
         
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
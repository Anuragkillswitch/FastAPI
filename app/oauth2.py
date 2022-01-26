
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

#Secret_key
#algorithm
#expiration time for auto-log out

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="Iu1sPs8y1XKpzRWbU5gDY2oMMplQrAqq7v2RzHzT3fPtoSafo4Bi8Kg"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data :dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
  
  
def verify_access_token(token:str,credentials_exception):
    
    try:
        
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")    

        if id is None:
            raise credentials_exception
    
        token_data=schema.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    
    return token_data
    
    
def get_current_user(token : str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=401,detail=f"Could not validate credentials"
                                        ,headers={"WWW-Authenticate":"Bearer"})  
    
    return verify_access_token(token,credentials_exception=credentials_exception)
  
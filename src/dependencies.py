from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional
from typing import Annotated
from src.database import SessionLocal
from src.auth.schemas import TokenData
from src.user.models import Users

SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except JWTError:
        raise credentials_exception
    print(token_data)
    user = db.query(Users).filter(Users.name == token_data.name).first()

    if user is None:
        raise credentials_exception
    return user

user_dependency = Annotated[dict, Depends(get_current_user)]

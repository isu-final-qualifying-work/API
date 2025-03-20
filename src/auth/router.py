from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from src.dependencies import get_db, pwd_context, create_access_token, get_current_user
from src.user.models import Users
from src.user.schemas import NewUser
from src.auth.schemas import Token, TokenData

router = APIRouter()

@router.post("/register", response_model=Token)
def register(request: NewUser, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == request.name).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(request.password)
    user = Users(name=request.name, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login_for_access_token(request: NewUser, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == request.name).one()
    if not user:
        return False
    if not pwd_context.verify(request.password, user.password):
        return False
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=NewUser)
def read_users_me(request=TokenData, db: Session = Depends(get_db)):
    user = get_current_user(db, request)
    return user

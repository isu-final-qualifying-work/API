from fastapi import APIRouter, Depends
from src.user.schemas import User, UserID, NewUser
from src.user.models import Users
from sqlalchemy.orm import Session
from src.dependencies import get_db
import hashlib

router = APIRouter()


@router.get("/users_all")
async def users_all(db: Session = Depends(get_db)):
    try:
        users = db.query(Users).all()
        return users
    except Exception as e:
        return {'message': e}
    
@router.post("/get_user")
async def get_user(request: UserID, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.id == request.id).all()
        return user
    except Exception as e:
        return {'message': e}

    
@router.post("/update_user")
async def update_user(request: User, db: Session = Depends(get_db)):
    try:
        db.query(Users).filter(Users.id == request.id).update({
            'name': request.name,
            'password': request.password
        })
        db.commit()
        return db.query(Users).filter(Users.id == request.id).all()
    except Exception as e:
        return {'message': e}
    

@router.delete("/delete_user")
async def delete_user(request: UserID, db: Session = Depends(get_db)):
    try:
        db.query(Users).filter(Users.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
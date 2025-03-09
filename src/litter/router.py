from fastapi import APIRouter, Depends
from src.litter.models import Litters, User_Litter
from src.litter.schemas import LitterID, NewLitter
from src.user.models import Users
from sqlalchemy.orm import Session
from src.dependencies import get_db

router = APIRouter()


@router.get("/litters_all")
async def litters_all(db: Session = Depends(get_db)):
    try:
        litters = db.query(Litters).all()
        return litters
    except Exception as e:
        return {'message': e}
    
@router.post("/get_litter")
async def get_litter(request: LitterID, db: Session = Depends(get_db)):
    try:
        litter = db.query(Litters).filter(Litters.id == request.id).all()
        return litter
    except Exception as e:
        return {'message': e}


@router.post("/add_litter")
async def add_litter(request: NewLitter, db: Session = Depends(get_db)):
    try:
        litter = Litters(name = request.name)
        user = db.query(Users).filter(Users.id == request.user_id).one()
        db.add(litter)
        litter_user = User_Litter(user_id = user.id, litter_id = litter.id)
        db.add(litter_user)
        db.commit()
        return litter
    except Exception as e:
        return {'message': e}
    
    
@router.delete("/delete_litter")
async def delete_litter(request: LitterID, db: Session = Depends(get_db)):
    try:
        db.query(Litters).filter(Litters.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
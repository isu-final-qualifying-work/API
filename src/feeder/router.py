from fastapi import APIRouter, Depends
from src.feeder.models import Feeders, User_Feeder
from src.feeder.schemas import NewFeeder, FeederID
from src.user.models import Users
from sqlalchemy.orm import Session
from src.dependencies import get_db

router = APIRouter()


@router.get("/feeders_all")
async def feeders_all(db: Session = Depends(get_db)):
    try:
        feeders = db.query(Feeders).all()
        return feeders
    except Exception as e:
        return {'message': e}
    
@router.post("/get_feeder")
async def get_feeder(request: FeederID, db: Session = Depends(get_db)):
    try:
        feeder = db.query(Feeders).filter(Feeders.id == request.id).all()
        return feeder
    except Exception as e:
        return {'message': e}


@router.post("/add_feeder")
async def add_feeder(request: NewFeeder, db: Session = Depends(get_db)):
    try:
        feeder = Feeders(name = request.name)
        user = db.query(Users).filter(Users.id == request.user_id).one()
        db.add(feeder)
        feeder_user = User_Feeder(user_id = user.id, feeder_id = feeder.id)
        db.add(feeder_user)
        db.commit()
        return feeder
    except Exception as e:
        return {'message': e}
    
    
@router.delete("/delete_feeder")
async def delete_feeder(request: FeederID, db: Session = Depends(get_db)):
    try:
        db.query(Feeders).filter(Feeders.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
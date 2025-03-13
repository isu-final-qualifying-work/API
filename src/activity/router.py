from fastapi import APIRouter, Depends
from src.activity.schemas import CollarActivity, NewCollarActivity, FeederFeed, NewFeederFeed
from src.activity.models import CollarsActivity, FeederFeeds
from src.collar.models import Collars
from src.feeder.models import Feeders
from sqlalchemy.orm import Session
from datetime import datetime
from src.dependencies import get_db

router = APIRouter()


@router.get("/collar_activity_all")
async def collar_activity_all(db: Session = Depends(get_db)):
    try:
        data = db.query(CollarsActivity).all()
        return data
    except Exception as e:
        return {'message': e}


@router.get("/feeder_feed_activity_all")
async def feeder_feed_activity_all(db: Session = Depends(get_db)):
    try:
        data = db.query(FeederFeeds).all()
        return data
    except Exception as e:
        return {'message': e}
    
@router.post("/collar_add_activity", response_model=NewCollarActivity)
async def collar_add_activity(request: CollarActivity, db: Session = Depends(get_db)):
    try:
        collar = db.query(Collars).where(Collars.name == request.collar).one()
        data = CollarsActivity(collar_id=collar.id, x=request.x, y=request.y, z=request.z, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}
    

@router.post("/feeder_feed_activity", response_model=NewFeederFeed)
async def feeder_feed_activity(request: FeederFeed, db: Session = Depends(get_db)):
    try:
        feeder = db.query(Feeders).where(Feeders.name == request.feeder).one()
        data = FeederFeeds(feeder_id=feeder.id, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}
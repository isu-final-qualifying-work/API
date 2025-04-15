from fastapi import APIRouter, Depends
from src.activity.schemas import CollarActivity, NewCollarActivity, Eating, NewEating, FeederFeed, NewFeederFeed, LitterClean, NewLitterClean
from src.activity.models import CollarsActivity, FeederFeeds, LitterCleans, EatingActivity
from src.collar.models import Collars
from src.feeder.models import Feeders
from src.litter.models import Litters
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
    
@router.get("/litter_clean_activity_all")
async def litter_clean_activity_all(db: Session = Depends(get_db)):
    try:
        data = db.query(LitterCleans).all()
        return data
    except Exception as e:
        return {'message': e}
    
@router.get("/eating_activity_all")
async def eating_activity_all(db: Session = Depends(get_db)):
    try:
        data = db.query(EatingActivity).all()
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
        
@router.post("/collar_add_activity", response_model=NewCollarActivity)
async def collar_add_activity(request: CollarActivity, db: Session = Depends(get_db)):
    try:
        collar = db.query(Collars).where(Collars.name == request.collar).one()
        data = CollarsActivity(collar_id=collar.id, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}
    
    
@router.post("/litter_clean_activity", response_model=NewLitterClean)
async def litter_clean_activity(request: LitterClean, db: Session = Depends(get_db)):
    try:
        litter = db.query(Litters).where(Litters.name == request.litter).one()
        collar = db.query(Collars).where(Collars.name == request.collar).one()
        data = LitterCleans(litter_id=litter.id, collar_id = collar.id, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}    
    
@router.post("/eating_activity", response_model=NewEating)
async def eating_activity(request: Eating, db: Session = Depends(get_db)):
    try:
        feeder = db.query(Feeders).where(Feeders.name == request.feeder).one()
        collar = db.query(Collars).where(Collars.name == request.collar).one()
        data = LitterCleans(feeder_id=feeder.id, collar_id = collar.id, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}
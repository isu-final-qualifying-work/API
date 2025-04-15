from fastapi import APIRouter, Depends
from src.feeder.models import Feeders, User_Feeder
from src.feeder.schemas import NewFeeder, FeederID, Feeder, FullFeederData
from src.user.models import Users
from src.collar.models import Collars
from src.setting.models import Settings
from src.user.schemas import UserID
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
from src.auth.schemas import Token

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


@router.post("/add_feeder", response_model=Feeder)
async def add_feeder(request: NewFeeder, db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, request.access_token)
        if(request.name.find("FEEDER_")):
            feeder = db.query(Feeders).filter(Feeders.name == request.name).first()
            if not feeder:
                feeder = Feeders(name=request.name)
                db.add(feeder)
                db.commit()
                settings = Settings(feeder_id=feeder.id)
                db.add(settings)
                db.commit()
            print(user.name, feeder.name)
            feeder_user = db.query(User_Feeder).filter_by(user_id=user.id, feeder_id=feeder.id).first()
            if not feeder_user:
                feeder_user = User_Feeder(user_id=user.id, feeder_id=feeder.id)
                db.add(feeder_user)
                db.commit()
                return {'id': feeder.id, 'name': feeder.name}
    except Exception as e:
        return {"message": str(e)}
    

@router.delete("/delete_feeder/{id}")
async def delete_feeder(id: int, db: Session = Depends(get_db)):
        try:
            db.query(User_Feeder).filter(User_Feeder.feeder_id == id).delete()
            db.query(Settings).filter(Settings.feeder_id == id).delete()
            db.query(Feeders).filter(Feeders.id == id).delete()
            db.commit()
            return {'message': 'ok'}
        except Exception as e:
            return {'message': e}
    
@router.post("/get_feeders_by_user")
async def get_feeders_by_user(request: Token, db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, request.access_token)
        data = []
        print(user)
        feeders = db.query(User_Feeder).filter(User_Feeder.user_id == user.id).all()
        for feeder in feeders:
            print(feeder.feeder_id, feeder.user_id)
            feed_elem = db.query(Feeders).filter(Feeders.id == feeder.feeder_id).one()
            elem = {
                'id': feed_elem.id,
                'name': feed_elem.name,
                'collars': []
            }
            print(feed_elem.collars)
            print(feed_elem.setting)
            if len(feed_elem.collars) > 0:
                for collar in feed_elem.collars:
                    print(collar.collar_id)
                    collar = db.query(Collars).filter(Collars.id == collar.collar_id).one()
                    elem['collars'].append(collar)
            setting = db.query(Settings).filter(Settings.feeder_id == feed_elem.id).one()

            elem["schedule"] = setting.schedule
            elem['timezone'] = setting.timezone
            elem['size'] = setting.size
            data.append(elem)
        return data
    except Exception as e:
        return {'message': e}
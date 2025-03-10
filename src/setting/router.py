from fastapi import APIRouter, Depends
from src.setting.models import Settings, Feeder_Settings
from src.setting.schemas import SettingID, NewSetting, Setting
from src.feeder.models import Feeders
from sqlalchemy.orm import Session
from src.dependencies import get_db

router = APIRouter()


@router.get("/settings_all")
async def settings_all(db: Session = Depends(get_db)):
    try:
        settings = db.query(Settings).all()
        return settings
    except Exception as e:
        return {'message': e}
    
@router.post("/get_settings")
async def get_settings(request: SettingID, db: Session = Depends(get_db)):
    try:
        settings = db.query(SettingID).filter(SettingID.id == request.id).all()
        return settings
    except Exception as e:
        return {'message': e}


@router.post("/add_settings")
async def add_settings(request: NewSetting, db: Session = Depends(get_db)):
    try:
        settings = Settings(size = request.size, schedule = request.schedule)
        feeder = db.query(Feeders).filter(Feeders.id == request.feeder_id).one()
        db.add(settings)
        settings_user = Feeder_Settings(setting_id = feeder.id, feeder_id = settings.id)
        db.add(settings_user)
        db.commit()
        return settings
    except Exception as e:
        return {'message': e}
    

@router.post("/update_settings")
async def update_settings(request: Setting, db: Session = Depends(get_db)):
    try:
        db.query(Settings).filter(Settings.id == request.id).update({
            'size': request.size,
            'schedule': request.schedule
        })
        db.commit()
        return db.query(Settings).filter(Settings.id == request.id).all()
    except Exception as e:
        return {'message': e}
        
@router.delete("/delete_settings")
async def delete_settings(request: SettingID, db: Session = Depends(get_db)):
    try:
        db.query(SettingID).filter(SettingID.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
from fastapi import APIRouter, Depends
from src.setting.models import Settings
from src.setting.schemas import SettingID, NewSetting, Setting, SettingByFeeder
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
        settings = db.query(Settings).filter(Settings.id == request.id).all()
        return settings
    except Exception as e:
        return {'message': e}
    

@router.post("/get_settings_by_feeder", response_model=Setting)
async def get_settings_by_feeder(request: SettingByFeeder, db: Session = Depends(get_db)):
    try:
        feeder = db.query(Feeders).filter(Feeders.name == request.feeder_name).one()
        print(feeder)
        settings = db.query(Settings).filter(Settings.id == feeder.setting).one()
        print(settings)
        return settings
    except Exception as e:
        return {'message': e}


# @router.post("/add_settings")
# async def add_settings(request: NewSetting, db: Session = Depends(get_db)):
#     try:
#         settings = Settings(size = request.size, schedule = request.schedule, timezone = request.timezone)
#         feeder = db.query(Feeders).filter(Feeders.id == request.feeder_id).one()
#         db.add(settings)
#         db.commit()
#         settings_user = Feeder_Settings(feeder_id = feeder.id, setting_id = settings.id)
#         db.add(settings_user)
#         db.commit()
#         return settings
#     except Exception as e:
#         return {'message': e}
    

# @router.post("/update_settings")
# async def update_settings(request: Setting, db: Session = Depends(get_db)):
#     try:
#         settings = db.query(Feeder_Settings).filter(request.id == Feeder_Settings.feeder_id).one()
#         print(request)
#         db.query(Settings).filter(settings.id == Settings.id).update({
#             'size': request.size,
#             'schedule': request.schedule,
#             'timezone': request.timezone
#         })
#         db.commit()
#         print(db.query(Settings).filter(settings.id == Settings.id).one())
#         return db.query(Settings).filter(Settings.id == settings.id).one()
#     except Exception as e:
#         return {'message': e}
        
@router.delete("/delete_settings")
async def delete_settings(request: SettingID, db: Session = Depends(get_db)):
    try:
        db.query(SettingID).filter(SettingID.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
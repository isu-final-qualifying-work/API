from fastapi import APIRouter, Depends
from src.collar.models import Collars, Feeder_Collar, Litter_Collar
from src.collar.schemas import Collar, CollarID, NewCollar
from src.feeder.models import Feeders
from src.litter.models import Litters
from sqlalchemy.orm import Session
from src.dependencies import get_db

router = APIRouter()


@router.get("/collars_all")
async def collars_all(db: Session = Depends(get_db)):
    try:
        collars = db.query(Collars).all()
        return collars
    except Exception as e:
        return {'message': e}
    
@router.post("/get_collar")
async def get_collar(request: CollarID, db: Session = Depends(get_db)):
    try:
        collar = db.query(Collars).filter(Collars.id == request.id).all()
        return collar
    except Exception as e:
        return {'message': e}


@router.post("/add_collar")
async def add_collar(request: NewCollar, db: Session = Depends(get_db)):
    try:
        collar = Collars(name = request.name)
        db.add(collar)
        if request.device_type == 'feeder':
            feeder = db.query(Feeders).filter(Feeders.id == request.device_id).one()
            feeder_collar = Feeder_Collar(feeder_id = feeder.id, collar_id = collar.id)
            db.add(feeder_collar)
        elif request.device_type == 'litter':
            litter = db.query(Litters).filter(Litters.id == request.device_id).one()
            litter_collar = Litter_Collar(litter_id = litter.id, collar_id = collar.id)
            db.add(litter_collar)
        db.commit()
        return collar
    except Exception as e:
        return {'message': e}
    
    
@router.delete("/delete_collar")
async def delete_collar(request: CollarID, db: Session = Depends(get_db)):
    try:
        db.query(Collars).filter(Collars.id == request.id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}

from fastapi import APIRouter, Depends
from src.collar.models import Collars, Feeder_Collar, Litter_Collar
from src.collar.schemas import Collar, CollarID, NewCollar, CollarByFeeder, CollarByLitter
from src.feeder.models import Feeders
from src.litter.models import Litters
from src.pet.models import Pets
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


@router.post("/get_collars_by_feeder")
async def get_collars_by_feeder(request: CollarByFeeder, db: Session = Depends(get_db)):
    try:
        feeder = db.query(Feeders).filter(Feeders.name == request.feeder_name).one()
        print(feeder)
        feeder_collars = db.query(Feeder_Collar).filter(Feeder_Collar.feeder_id == feeder.id).all()
        print(feeder_collars)
        collars = []
        for feeder_collar in feeder_collars:
            print(feeder_collar.collar_id)
            collar = db.query(Collars).filter(Collars.id == feeder_collar.collar_id).one()
            
            print(collar)
            collars.append(collar.name)
        return collars
    except Exception as e:
        return {'message': e}


@router.post("/get_collars_by_litter")
async def get_collars_by_litter(request: CollarByLitter, db: Session = Depends(get_db)):
    try:
        litter = db.query(Litters).filter(Litters.name == request.litter_name).all()[0]
        print(litter)
        litter_collars = db.query(Litter_Collar).filter(Litter_Collar.litter_id == litter.id).all()
        print(litter_collars)
        collars = []
        for litter_collar in litter_collars:
            print(litter_collar.collar_id)
            collar = db.query(Collars).filter(Collars.id == litter_collar.collar_id).one()
            
            print(collar)
            collars.append(collar.name)
        return collars
    except Exception as e:
        return {'message': e}    


@router.post("/add_collar", response_model=Collar)
async def add_collar(request: NewCollar, db: Session = Depends(get_db)):
    try:
        collar = db.query(Collars).filter(Feeders.name == request.name).first()
        if not collar:
            collar = Collars(name = request.name)
            db.add(collar)
            db.commit()
        if request.device_type == 'feeder':
            feeder = db.query(Feeders).filter(Feeders.id == request.device_id).one()
            feeder_collar = Feeder_Collar(feeder_id = feeder.id, collar_id = collar.id)
            db.add(feeder_collar)
        elif request.device_type == 'litter':
            litter = db.query(Litters).filter(Litters.id == request.device_id).one()
            litter_collar = Litter_Collar(litter_id = litter.id, collar_id = collar.id)
            db.add(litter_collar)
        db.commit()
        if request.child == True:
            pet = Pets(name=request.pet_name, type=request.type, collar_id=collar.id, gender=request.gender, is_child=request.child, weight=request.weight, is_pregnant=False, is_sterilized=False)
        else:
            pet = Pets(name=request.pet_name, type=request.type, collar_id=collar.id, gender=request.gender, is_child=request.child, weight=request.weight, is_pregnant=request.pregnant, is_sterilized=request.sterilized)
        db.add(pet)
        db.commit()
        print(pet)
        return {'id': collar.id, 'name': collar.name}
        return collar
    except Exception as e:
        return {'message': e}
    
    
@router.delete("/delete_collar/{id}")
async def delete_collar(id: int, db: Session = Depends(get_db)):
    try:
        db.query(Litter_Collar).filter(Litter_Collar.collar_id == id).delete()
        db.query(Feeder_Collar).filter(Feeder_Collar.collar_id == id).delete()
        db.query(Pets).filter(Pets.collar_id == id).delete()
        db.query(Collars).filter(Collars.id == id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
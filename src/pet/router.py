from fastapi import APIRouter, Depends
from src.pet.models import Pets
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
from src.auth.schemas import Token
from sqlalchemy import select, union_all
from src.pet.models import Pets
from src.collar.models import Collars, Feeder_Collar, Litter_Collar
from src.feeder.models import User_Feeder, Feeders
from src.litter.models import User_Litter, Litters
from src.auth.schemas import Token
from src.pet.schemas import NewPet, Pet
from src.collar.schemas import CollarID
router = APIRouter()


@router.get("/pets_all")
async def pets_all(db: Session = Depends(get_db)):
    try:
        feeders = db.query(Pets).all()
        return feeders
    except Exception as e:
        return {'message': e}
    

router = APIRouter()
@router.post("/get_pets_by_user")
def get_pets_by_user(request: Token, db: Session = Depends(get_db)):
    user = get_current_user(db, request.access_token)

    feeders = (
        db.query(Pets.id.label("id"), Pets.name.label("name"))
        .join(Collars, Pets.collar_id == Collars.id)
        .join(Feeder_Collar, Feeder_Collar.collar_id == Collars.id)
        .join(Feeders, Feeders.id == Feeder_Collar.feeder_id)
        .join(User_Feeder, User_Feeder.feeder_id == Feeders.id)
        .filter(User_Feeder.user_id == user.id)
    )

    litters = (
        db.query(Pets.id.label("id"), Pets.name.label("name"))
        .join(Collars, Pets.collar_id == Collars.id)
        .join(Litter_Collar, Litter_Collar.collar_id == Collars.id)
        .join(Litters, Litters.id == Litter_Collar.litter_id)
        .join(User_Litter, User_Litter.litter_id == Litters.id)
        .filter(User_Litter.user_id == user.id)
    )

    query = feeders.union_all(litters).subquery()

    results = db.query(query.c.id, query.c.name).all()

    return [{"id": row.id, "name": row.name} for row in results]


@router.post("/update_pet")
async def update_pet(request: NewPet, db: Session = Depends(get_db)):
    try:
        pets = db.query(Pets).where(request.collar_id == Pets.collar_id).one()
        print(request)
        db.query(Pets).filter(pets.id == Pets.id).update({
            'name': request.name,
            'gender': request.gender,
            'type': request.type,
            'is_child': request.is_child,
            'weight': request.weight,
            'is_pregnant': request.is_pregnant,
            'is_sterilized': request.is_sterilized
        })
        db.commit()
        print(db.query(Pets).filter(Pets.id == Pets.id).one())
        return db.query(Pets).filter(Pets.id == Pets.id).one()
    except Exception as e:
        return {'message': e}
        

@router.post("/get_pet", response_model=Pet)
async def update_pet(request: CollarID, db: Session = Depends(get_db)):
    try:
        pet = db.query(Pets).where(request.id == Pets.collar_id).one()
        return {
            'id': pet.id,
            'name': pet.name,
            'gender': pet.gender,
            'type': pet.type,
            'is_child': pet.is_child,
            'weight': pet.weight,
            'is_pregnant': pet.is_pregnant,
            'is_sterilized': pet.is_sterilized,
            'collar_id': request.id
        }
    except Exception as e:
        return {'message': e}
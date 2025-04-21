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

    subquery_feeders = (
        db.query(Pets.id.label("id"), Pets.name.label("name"))
        .join(Collars, Pets.collar_id == Collars.id)
        .join(Feeder_Collar, Feeder_Collar.collar_id == Collars.id)
        .join(Feeders, Feeders.id == Feeder_Collar.feeder_id)
        .join(User_Feeder, User_Feeder.feeder_id == Feeders.id)
        .filter(User_Feeder.user_id == user.id)
    )

    subquery_litters = (
        db.query(Pets.id.label("id"), Pets.name.label("name"))
        .join(Collars, Pets.collar_id == Collars.id)
        .join(Litter_Collar, Litter_Collar.collar_id == Collars.id)
        .join(Litters, Litters.id == Litter_Collar.litter_id)
        .join(User_Litter, User_Litter.litter_id == Litters.id)
        .filter(User_Litter.user_id == user.id)
    )

    union_query = subquery_feeders.union_all(subquery_litters).subquery()

    results = db.query(union_query.c.id, union_query.c.name).all()

    return [{"id": row.id, "name": row.name} for row in results]
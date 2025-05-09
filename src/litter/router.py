from fastapi import APIRouter, Depends
from src.litter.models import Litters, User_Litter
from src.litter.schemas import LitterID, NewLitter, Litter
from src.user.models import Users
from src.user.schemas import UserID
from src.collar.models import Collars
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
from src.auth.schemas import Token

router = APIRouter()


@router.get("/litters_all")
async def litters_all(db: Session = Depends(get_db)):
    try:
        litters = db.query(Litters).all()
        return litters
    except Exception as e:
        return {'message': e}
    
@router.post("/get_litter")
async def get_litter(request: LitterID, db: Session = Depends(get_db)):
    try:
        litter = db.query(Litters).filter(Litters.id == request.id).all()
        return litter
    except Exception as e:
        return {'message': e}


@router.post("/add_litter", response_model=Litter)
async def add_litter(request: NewLitter, db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, request.access_token)
        litter = db.query(Litters).filter(Litters.name == request.name).first()
        if not litter:
            litter = Litters(name=request.name)
            db.add(litter)
            db.commit()
        litter_user = db.query(User_Litter).filter_by(user_id=user.id, litter_id=litter.id).first()
        if not litter_user:
            litter_user = User_Litter(user_id=user.id, litter_id=litter.id)
            db.add(litter_user)
            db.commit()
            return {'id': litter.id, 'name': litter.name}
    except Exception as e:
        return {"message": str(e)}
    
    
@router.delete("/delete_litter/{id}")
async def delete_litter(id: int, db: Session = Depends(get_db)):
    try:
        db.query(User_Litter).filter(User_Litter.litter_id == id).delete()
        db.query(Litters).filter(Litters.id == id).delete()
        db.commit()
        return {'message': 'ok'}
    except Exception as e:
        return {'message': e}
    

    
@router.post("/get_litters_by_user")
async def get_litters_by_user(request: Token, db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, request.access_token)
        data = []
        litters = db.query(User_Litter).filter(User_Litter.user_id == user.id).all()
        for litter in litters:
            print(litter.litter_id, litter.user_id)
            lit_elem = db.query(Litters).filter(Litters.id == litter.litter_id).one()
            print(lit_elem.name)
            elem = {
                'id': lit_elem.id,
                'name': lit_elem.name,
                'collars': []
            }
            print(elem)
            if len(lit_elem.collars) > 0:
                for collar in lit_elem.collars:
                    print(collar.collar_id)
                    collar = db.query(Collars).filter(Collars.id == collar.collar_id).one()
                    elem['collars'].append(collar)
            data.append(elem)
        return data
    except Exception as e:
        return {'message': e}
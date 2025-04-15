from fastapi import APIRouter, Depends
from src.analitic.schemas import EatingActivityFilter
from src.activity.models import EatingActivity
from src.collar.models import Collars
from src.feeder.models import Feeders
from src.litter.models import Litters
from src.pet.models import Pets
from sqlalchemy.orm import Session
from datetime import datetime
from src.dependencies import get_db

from sqlalchemy import extract, func

router = APIRouter()

@router.post("/get_eating_activity")
async def get_eating_activity(request: EatingActivityFilter, db: Session = Depends(get_db)):
    try:
        collar = db.query(Pets).where(Pets.id == request.pet_id).one()
        if request.type == 'all':
            data = db.query(EatingActivity).where(
                EatingActivity.collar_id == collar.collar_id
            ).all()
            return data

        elif request.type == 'day':
            data = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.size).label('size')
            ).where(
                EatingActivity.collar_id == collar.collar_id
            ).group_by(func.date(EatingActivity.datetime)).all()

            return [{'day': str(row.day), 'size': float(row.size)} for row in data]

        elif request.type == 'month':
            data = db.query(
                extract('year', EatingActivity.datetime).label('year'),
                extract('month', EatingActivity.datetime).label('month'),
                func.sum(EatingActivity.size).label('size')
            ).where(
                EatingActivity.collar_id == collar.collar_id
            ).group_by('year', 'month').order_by('year', 'month').all()

            return [{'year': int(row.year), 'month': int(row.month), 'size': float(row.size)} for row in data]

        elif request.type == 'year':
            data = db.query(
                extract('year', EatingActivity.datetime).label('year'),
                func.sum(EatingActivity.size).label('size')
            ).where(
                EatingActivity.collar_id == collar.collar_id
            ).group_by('year').order_by('year').all()

            return [{'year': int(row.year), 'size': float(row.size)} for row in data]

        return {'message': 'Unknown type'}

    except Exception as e:
        return {'message': str(e)}

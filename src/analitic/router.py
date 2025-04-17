from fastapi import APIRouter, Depends
from src.analitic.schemas import ActivityFilter
from src.activity.models import EatingActivity, LitterCleans, CollarsActivity
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
async def get_eating_activity(request: ActivityFilter, db: Session = Depends(get_db)):
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

@router.post("/get_litter_clean_activity")
async def get_litter_clean_activity(request: ActivityFilter, db: Session = Depends(get_db)):
    try:
        collar = db.query(Pets).where(Pets.id == request.pet_id).one()
        if request.type == 'all':
            data = db.query(LitterCleans).where(
                LitterCleans.collar_id == collar.collar_id
            ).all()
            return data

        elif request.type == 'day':
            data = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).where(
                LitterCleans.collar_id == collar.collar_id
            ).group_by(func.date(LitterCleans.datetime)).all()

            return [{'day': str(row.day), 'count': float(row.count)} for row in data]

        elif request.type == 'month':
            data = db.query(
                extract('year', LitterCleans.datetime).label('year'),
                extract('month', LitterCleans.datetime).label('month'),
                func.count(LitterCleans.id).label('count')
            ).where(
                LitterCleans.collar_id == collar.collar_id
            ).group_by('year', 'month').order_by('year', 'month').all()

            return [{'year': int(row.year), 'month': int(row.month), 'count': float(row.count)} for row in data]

        elif request.type == 'year':
            data = db.query(
                extract('year', LitterCleans.datetime).label('year'),
                func.count(LitterCleans.size).label('count')
            ).where(
                LitterCleans.collar_id == collar.collar_id
            ).group_by('year').order_by('year').all()

            return [{'year': int(row.year), 'count': float(row.count)} for row in data]

        return {'message': 'Unknown type'}

    except Exception as e:
        return {'message': str(e)}
    

@router.post("/get_collar_activity")
async def get_collar_activity(request: ActivityFilter, db: Session = Depends(get_db)):
    try:
        collar = db.query(Pets).where(Pets.id == request.pet_id).one()
        if request.type == 'all':
            data = db.query(CollarsActivity).where(
                CollarsActivity.collar_id == collar.collar_id
            ).all()
            return data

        elif request.type == 'day':
            data = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).where(
                CollarsActivity.collar_id == collar.collar_id
            ).group_by(func.date(CollarsActivity.datetime)).all()

            return [{'day': str(row.day), 'count': float(row.count)} for row in data]

        elif request.type == 'month':
            data = db.query(
                extract('year', CollarsActivity.datetime).label('year'),
                extract('month', CollarsActivity.datetime).label('month'),
                func.count(CollarsActivity.id).label('count')
            ).where(
                CollarsActivity.collar_id == collar.collar_id
            ).group_by('year', 'month').order_by('year', 'month').all()

            return [{'year': int(row.year), 'month': int(row.month), 'count': float(row.count)} for row in data]

        elif request.type == 'year':
            data = db.query(
                extract('year', CollarsActivity.datetime).label('year'),
                func.count(CollarsActivity.size).label('count')
            ).where(
                CollarsActivity.collar_id == collar.collar_id
            ).group_by('year').order_by('year').all()

            return [{'year': int(row.year), 'count': float(row.count)} for row in data]

        return {'message': 'Unknown type'}

    except Exception as e:
        return {'message': str(e)}
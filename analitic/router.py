from fastapi import APIRouter, Depends
from src.analitic.schemas import ActivityFilter
from src.activity.models import EatingActivity, LitterCleans, CollarsActivity
from src.collar.models import Collars
from src.feeder.models import Feeders
from src.litter.models import Litters
from src.analitic.models import EatingKoef, LitterReference, ActivityReference
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
        if request.type == 'day':
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
        if request.type == 'day':
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
        if request.type == 'day':
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
    
@router.post("/check_references")
async def check_references(request: ActivityFilter, db: Session = Depends(get_db)):
    messages = []
    pet = db.query(Pets).where(Pets.id == request.pet_id).one()
    if pet.is_child == True:
        eating = db.query(EatingKoef).where(EatingKoef.type == pet.type and EatingKoef.category == 'child').one()
        litter = db.query(LitterReference).where(LitterReference.type == pet.type and LitterReference.is_child == True).one()
        activity = db.query(ActivityReference).where(ActivityReference.type == pet.type and ActivityReference.is_child == True).one()
    elif pet.is_pregnant == True:
        eating = db.query(EatingKoef).where(EatingKoef.type == pet.type and EatingKoef.category == 'pregnant').one()
        litter = db.query(LitterReference).where(LitterReference.type == pet.type and LitterReference.is_pregnant == True).one()
        activity = db.query(ActivityReference).where(ActivityReference.type == pet.type and ActivityReference.is_pregnant == True).one()
    elif pet.is_sterilized == True:
        eating = db.query(EatingKoef).where(EatingKoef.type == pet.type and EatingKoef.category == 'sterilized').one()
        litter = db.query(LitterReference).where(LitterReference.type == pet.type and LitterReference.gender == pet.gender and LitterReference.is_sterilized == pet.is_sterilized).one()
        activity = db.query(ActivityReference).where(ActivityReference.type == pet.type and ActivityReference.gender == pet.gender and ActivityReference.is_sterilized == pet.is_sterilized).one()
    else:
        eating = db.query(EatingKoef).where(EatingKoef.type == pet.type and EatingKoef.category == 'basic').one()
        litter = db.query(LitterReference).where(LitterReference.type == pet.type and LitterReference.gender == pet.gender and LitterReference.is_sterilized == False and LitterReference.is_pregnant == False).one()
        activity = db.query(ActivityReference).where(ActivityReference.type == pet.type and ActivityReference.gender == pet.gender and ActivityReference.is_sterilized == False and ActivityReference.is_pregnant == False).one()
    eating_size = db.query(func.sum(EatingActivity.size).label('size')).where(EatingActivity.datetime == datetime.today() - 1).one()
    litter_size = db.query(func.count(LitterCleans.id).label('count')).where(LitterCleans.datetime == datetime.today() - 1).one()
    activity_size = db.query(func.count(CollarsActivity.id).label('count')).where(CollarsActivity.datetime == datetime.today() - 1).one()
    if pet == 'dog':
        min_eating = (((70 * pet.weight)^(0.75))*eating.min)/380
        max_eating = (((70 * pet.weight)^(0.75))*eating.max)/380
    if pet == 'cat':
        min_eating = ((pet.weight^(0.75))*eating.min)/350
        max_eating = ((pet.weight^(0.75))*eating.max)/350
    if eating_size.size > max_eating:
        messages.append(f"Питомец {pet.name} слишком много питается, что может привести к ожирению. Скорректируйте потребление корма  диапазоне {min_eating}-{max_eating}гр.")
    elif eating_size.size < min_eating:
        messages.append(f"Питомец {pet.name} слишком мало питается. Это может указывать на проблемы со здоровьем, стресс или некорректный размер порции. Скорректируйте потребление корма  диапазоне {min_eating}-{max_eating}гр. или обратитесь к ветеринару.")
    
    if litter_size.count < litter.min:
        messages.append(f"Питомец {pet.name} мало ходит в туалет. Это может указывать на проблемы со здоровьем, стресс или непринятие лотка. Рекомендуем обратиться к ветеринару.")
    elif eating_size.size > litter.max:
        messages.append(f"Питомец {pet.name} много ходит в туалет. Это может указывать на проблемы со здоровьем или стресс. Рекомендуем обратиться к ветеринару.")
        
    if activity_size.count > activity.min:
        messages.append(f"Питомец {pet.name} мало двигается. Это может указывать на проблемы со здоровьем, стресс или возрастные изменения. Рекомендуем обратиться к ветеринару.")
    return messages
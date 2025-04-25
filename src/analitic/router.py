from fastapi import APIRouter, Depends
from src.analitic.schemas import ActivityFilter
from src.activity.models import EatingActivity, LitterCleans, CollarsActivity
from src.collar.models import Collars
from src.feeder.models import Feeders
from src.litter.models import Litters
from src.analitic.models import EatingKoef, LitterReference, ActivityReference
from src.pet.models import Pets
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
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
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == collar.collar_id,
                func.date(EatingActivity.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(EatingActivity.datetime)).all()
        elif request.type == 'week':
            data = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == collar.collar_id,
                func.date(EatingActivity.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(EatingActivity.datetime)).all()
        elif request.type == 'month':
            data = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == collar.collar_id,
                func.date(EatingActivity.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(EatingActivity.datetime)).all()
        print(data)
        return [{'day': str(row.day), 'size': float(row.count)} for row in data]

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
            ).filter(
                LitterCleans.collar_id == collar.collar_id,
                func.date(LitterCleans.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(LitterCleans.datetime)).all()
        elif request.type == 'week':
            data = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).filter(
                LitterCleans.collar_id == collar.collar_id,
                func.date(LitterCleans.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(LitterCleans.datetime)).all()
        elif request.type == 'month':
            data = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).filter(
                LitterCleans.collar_id == collar.collar_id,
                func.date(LitterCleans.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(LitterCleans.datetime)).all()
        print(data)
        return [{'day': str(row.day), 'count': float(row.count)} for row in data]
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
            ).filter(
                CollarsActivity.collar_id == collar.collar_id,
                func.date(CollarsActivity.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(CollarsActivity.datetime)).all()
        elif request.type == 'week':
            data = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).filter(
                CollarsActivity.collar_id == collar.collar_id,
                func.date(CollarsActivity.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(CollarsActivity.datetime)).all()
        elif request.type == 'month':
            data = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).filter(
                CollarsActivity.collar_id == collar.collar_id,
                func.date(CollarsActivity.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(CollarsActivity.datetime)).all()
        print(data)
        return [{'day': str(row.day), 'count': float(row.count)} for row in data]

    except Exception as e:
        return {'message': str(e)}
    
@router.post("/check_references")
async def check_references(request: ActivityFilter, db: Session = Depends(get_db)):
    messages = []
    pet = db.query(Pets).where(Pets.id == request.pet_id).one()
    if pet.is_child == True:
        eating = db.query(EatingKoef).filter(EatingKoef.type == pet.type, EatingKoef.category == 'child').one()
        litter = db.query(LitterReference).filter(LitterReference.type == pet.type, LitterReference.is_child == True).one()
        activity = db.query(ActivityReference).filter(ActivityReference.type == pet.type, ActivityReference.is_child == True).one()
    elif pet.is_pregnant == True:
        eating = db.query(EatingKoef).filter(EatingKoef.type == pet.type, EatingKoef.category == 'pregnant').one()
        litter = db.query(LitterReference).filter(LitterReference.type == pet.type, LitterReference.is_pregnant == True).one()
        activity = db.query(ActivityReference).filter(ActivityReference.type == pet.type, ActivityReference.is_pregnant == True).one()
    elif pet.is_sterilized == True:
        eating = db.query(EatingKoef).filter(EatingKoef.type == pet.type, EatingKoef.category == 'sterilized').one()
        litter = db.query(LitterReference).filter(LitterReference.type == pet.type, LitterReference.gender == pet.gender.lower(), LitterReference.is_sterilized == pet.is_sterilized).one()
        activity = db.query(ActivityReference).filter(ActivityReference.type == pet.type, ActivityReference.gender == pet.gender.lower(), ActivityReference.is_sterilized == pet.is_sterilized).one()
    else:
        eating = db.query(EatingKoef).filter(EatingKoef.type == pet.type, EatingKoef.category == 'basic').one()
        if pet.gender == "M":
            litter = db.query(LitterReference).filter(LitterReference.type == pet.type, LitterReference.gender == pet.gender.lower(), LitterReference.is_sterilized == False).one()
            activity = db.query(ActivityReference).filter(ActivityReference.type == pet.type, ActivityReference.gender == pet.gender.lower(), ActivityReference.is_sterilized == False).one()
        else:
            litter = db.query(LitterReference).filter(LitterReference.type == pet.type, LitterReference.gender == pet.gender.lower(), LitterReference.is_sterilized == False, LitterReference.is_pregnant == False).one()
            activity = db.query(ActivityReference).filter(ActivityReference.type == pet.type, ActivityReference.gender == pet.gender.lower(), ActivityReference.is_sterilized == False, ActivityReference.is_pregnant == False).one()
    print(type(EatingActivity.datetime))
    if request.type == "day":   
        eating_size = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == pet.collar_id,
                func.date(EatingActivity.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(EatingActivity.datetime)).order_by(
    func.date(EatingActivity.datetime)
).all()
        litter_size = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).filter(
                LitterCleans.collar_id == pet.collar_id,
                func.date(LitterCleans.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(LitterCleans.datetime)).order_by(
    func.date(LitterCleans.datetime)
).all()
        activity_size = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).filter(
                CollarsActivity.collar_id == pet.collar_id,
                func.date(CollarsActivity.datetime) == date.today() - timedelta(days=1)
            ).group_by(func.date(CollarsActivity.datetime)).order_by(
    func.date(CollarsActivity.datetime)
).all()
    elif request.type == "week":   
        eating_size = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(EatingActivity.datetime)).order_by(
    func.date(EatingActivity.datetime)
).all()
        litter_size = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).filter(
                LitterCleans.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(LitterCleans.datetime)).order_by(
    func.date(LitterCleans.datetime)
).all()
        activity_size = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).filter(
                CollarsActivity.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=7), date.today() - timedelta(days=1)),
            ).group_by(func.date(CollarsActivity.datetime)).order_by(
    func.date(CollarsActivity.datetime)
).all()
    elif request.type == "month":   
        eating_size = db.query(
                func.date(EatingActivity.datetime).label('day'),
                func.sum(EatingActivity.id).label('size')
            ).filter(
                EatingActivity.collar_id == pet.collar_id,CollarsActivity.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(EatingActivity.datetime)).order_by(
    func.date(EatingActivity.datetime)
).all()
        litter_size = db.query(
                func.date(LitterCleans.datetime).label('day'),
                func.count(LitterCleans.id).label('count')
            ).filter(
                LitterCleans.collar_id == pet.collar_id,
                LitterCleans.collar_id == pet.collar_id,CollarsActivity.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(LitterCleans.datetime)).order_by(
    func.date(LitterCleans.datetime)
).all()
        activity_size = db.query(
                func.date(CollarsActivity.datetime).label('day'),
                func.count(CollarsActivity.id).label('count')
            ).filter(
                CollarsActivity.collar_id == pet.collar_id,
                CollarsActivity.collar_id == pet.collar_id,CollarsActivity.collar_id == pet.collar_id,func.date(LitterCleans.datetime).between(date.today() - timedelta(days=30), date.today() - timedelta(days=1)),
            ).group_by(func.date(CollarsActivity.datetime)).order_by(
    func.date(CollarsActivity.datetime)
).all()
    if pet.type == 'dog':
        rer = pow(pet.weight, 0.75) * 70
        min_eating = (rer*float(eating.min))/380
        max_eating = (rer*float(eating.max))/380
    if pet.type == 'cat':
        rer = pow(pet.weight, 0.75) * 100
        min_eating = (rer*float(eating.min))/350
        max_eating = (rer*float(eating.max))/350
    for eating_elem in eating_size:
        print(eating_elem.size)
        if eating_elem.size > max_eating:
            messages.append(f"{eating_elem.day}: Питомец {pet.name} слишком много питается, что может привести к ожирению. Скорректируйте потребление корма в диапазоне {int(min_eating)}-{int(max_eating)}гр.")
        elif eating_elem.size < min_eating:
            messages.append(f"{eating_elem.day}: Питомец {pet.name} слишком мало питается. Это может указывать на проблемы со здоровьем, стресс или некорректный размер порции. Скорректируйте потребление корма  диапазоне {int(min_eating)}-{int(max_eating)}гр. или обратитесь к ветеринару.")
     
    for litter_elem in litter_size: 
        
        print(litter_elem.count)  
        if litter_elem.count < litter.min:
            messages.append(f"{litter_elem.day}: Питомец {pet.name} мало ходит в туалет. Это может указывать на проблемы со здоровьем, стресс или непринятие лотка. Рекомендуем обратиться к ветеринару.")
        elif litter_elem.count > litter.max:
            messages.append(f"{litter_elem.day}: Питомец {pet.name} много ходит в туалет. Это может указывать на проблемы со здоровьем или стресс. Рекомендуем обратиться к ветеринару.")
  
    for activity_elem in activity_size:   
        
        print(activity_elem.count)      
        if activity_elem.count < activity.min:
            messages.append(f"{activity_elem.day}: Питомец {pet.name} мало двигается. Это может указывать на проблемы со здоровьем, стресс или возрастные изменения. Рекомендуем обратиться к ветеринару.")
    return messages
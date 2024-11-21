from fastapi import APIRouter, Depends
from src.activity.schemas import CollarActivity, NewCollarActivity
from src.activity.models import CollarsActivity
from sqlalchemy.orm import Session
from datetime import datetime
from src.dependencies import get_db

router = APIRouter()


@router.get("/activity_all")
async def activity_all(db: Session = Depends(get_db)):
    try:
        collars = db.query(CollarsActivity).all()
        return collars
    except Exception as e:
        return {'message': e}


@router.post("/add_activity", response_model=NewCollarActivity)
async def add_activity(request: CollarActivity, db: Session = Depends(get_db)):
    try:
        data = CollarsActivity(collar=request.collar, x=request.x, y=request.y, z=request.z, datetime=datetime.now())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return {'message': e}
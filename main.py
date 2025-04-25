import uvicorn
from fastapi import FastAPI
from src.database import engine, Base
from src.activity.router import router as activity_router
from src.user.router import router as user_router
from src.feeder.router import router as feeder_router
from src.litter.router import router as litter_router
from src.setting.router import router as settings_router
from src.collar.router import router as collar_router
from src.auth.router import router as auth_router
from src.analitic.router import router as analitic_router
from src.pet.router import router as pet_router
from src.pet.models import Pets
from src.user.models import Users
from src.feeder.models import Feeders
from src.litter.models import Litters
from src.analitic.schemas import ActivityFilter
from src.analitic.router import check_references

from src.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from email.message import EmailMessage
import aiosmtplib

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.config.env import DICT_ENVS

EMAIL_HOST = DICT_ENVS['EMAIL_HOST']
EMAIL_PORT = DICT_ENVS['EMAIL_PORT']
EMAIL_USERNAME = DICT_ENVS['EMAIL_USERNAME']
EMAIL_PASSWORD = DICT_ENVS['EMAIL_PASSWORD']

server = FastAPI()

Base.metadata.create_all(engine)


server = FastAPI()
server.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"]
)

server.include_router(activity_router, prefix='/activity')
server.include_router(user_router, prefix='/user')
server.include_router(feeder_router, prefix='/feeder')
server.include_router(litter_router, prefix='/litter')
server.include_router(settings_router, prefix='/settings')
server.include_router(collar_router, prefix='/collar')
server.include_router(analitic_router, prefix='/analitic')
server.include_router(pet_router, prefix='/pet')
server.include_router(auth_router)


async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = EMAIL_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        start_tls=True,
        username=EMAIL_USERNAME,
        password=EMAIL_PASSWORD
    )


async def send_reports():
    db: Session = get_db()
    users = db.query(Users).all()

    for user in users:
        user_feeders = db.query(Feeders).filter(Feeders.user_id == user.id).all()
        user_litters = db.query(Litters).filter(Litters.user_id == user.id).all()

        feeder_collars = [feeder.collars for feeder in user_feeders if feeder.collars]
        litter_collars = [litter.collars for litter in user_litters if litter.collars]
        collars = set(feeder_collars + litter_collars)
        pets = db.query(Pets).filter(Pets.collar_id.in_(collars)).all()
        if not pets:
            continue

        report = ""
        for pet in pets:
            payload = ActivityFilter(pet_id=pet.id, type="day")
            result = await check_references(payload, db)
            report += f"Питомец: {pet.name}:\n"
            for res in result:
                report += (f"{res}\n")

        if report:
            await send_email(user.email, "PET HOME: Aналитика по питомцам", report)


scheduler = AsyncIOScheduler()

@server.on_event("startup")
async def startup_event():
    scheduler.add_job(send_reports, "interval", hours=24)
    scheduler.start()

@server.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run(server, host='0.0.0.0', port=8000)
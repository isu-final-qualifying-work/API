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

from fastapi.middleware.cors import CORSMiddleware


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
server.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(server, host='0.0.0.0', port=8000)
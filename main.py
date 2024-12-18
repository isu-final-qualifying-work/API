import uvicorn
from fastapi import FastAPI
from src.database import engine, Base
from src.activity.router import router as activity_router


server = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

server = FastAPI()
server.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
server.include_router(activity_router)

if __name__ == "__main__":
    uvicorn.run(server, host='0.0.0.0', port=8000)
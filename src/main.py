from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from app.routers import api_router


app = FastAPI(
    title='UDV Кафетерий льгот'
)

app.include_router(api_router)


origins = [
    settings.LOCAL_ORIGIN,
    settings.MAIN_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

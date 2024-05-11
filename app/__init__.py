from fastapi import Depends, FastAPI
from .endpoints.analyse import v1_router
from app.lib.parse_conf import set_env
from fastapi.middleware.cors import CORSMiddleware
import logging


set_env()

format = "%(asctime)s | %(lineno)d | %(levelname)s | %(funcName)s | %(message)s"
logging.basicConfig(level=logging.DEBUG, format=format)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)

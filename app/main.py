import os
from fastapi import FastAPI
from dotenv import load_dotenv

from app.config.db import init_db
from app.routes.order_routes import router

load_dotenv()

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
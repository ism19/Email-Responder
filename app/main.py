from fastapi import FastAPI
from app.routes import email_routes, syllabus
from app.services.polling import poll_gmail
import asyncio
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(poll_gmail (
        os.environ.get("PROFESSOR_EMAIL"),
        os.environ.get("USER_ID")
    ))
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(email_routes.router)
app.include_router(syllabus.router)

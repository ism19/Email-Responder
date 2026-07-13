from fastapi import FastAPI
from app.routes import email_routes, syllabus, auth
from app.services.polling import poll_gmail
import asyncio
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.database.database import init_db, get_all_professors

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    professors = await get_all_professors()
    for prof in professors:
        token_data = {
            "token": prof["access_token"],
            "refresh_token": prof["refresh_token"],
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
        }
        asyncio.create_task(poll_gmail (
        professor_email=prof["email"],
        user_id=prof["google_id"],
        token_data=token_data
        ))
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(email_routes.router)
app.include_router(syllabus.router)
app.include_router(auth.router)

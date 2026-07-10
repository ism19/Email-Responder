from fastapi import FastAPI
import email, syllabus

app = FastAPI()

app.include_router(email.router)
app.include_router(syllabus.router)
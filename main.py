from fastapi import FastAPI
import email_routes, syllabus

app = FastAPI()

app.include_router(email_routes.router)
app.include_router(syllabus.router)
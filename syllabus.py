from fastapi import APIRouter, UploadFile, File
from ingestion import ingest_syllabus

router = APIRouter()

@router.post("/upload-syllabus")
async def upload_syllabus (
    file: UploadFile = File(...),
    user_id: str = "test_prof"
):
    contents = await file.read()
    ingest_syllabus(pdf=contents, user_id=user_id)
    return {"status": "syllabus indexed"}
from fastapi import APIRouter, UploadFile, File, Depends
from app.rag.ingestion import ingest_syllabus
from app.auth.dependencies import get_current_professor

router = APIRouter()

@router.post("/upload-syllabus")
async def upload_syllabus (
    file: UploadFile = File(...),
    professor = Depends(get_current_professor)
):
    contents = await file.read()
    user_id = professor["google_id"]
    ingest_syllabus(pdf=contents, user_id=user_id)
    return {"status": "syllabus indexed"}
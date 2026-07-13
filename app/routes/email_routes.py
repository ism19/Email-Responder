from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.agent.graph import agent
from app.auth.dependencies import get_current_professor

router = APIRouter()

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str

@router.post("/process-email")
async def process_email(email: EmailInput, professor = Depends(get_current_professor)):
    result = agent.invoke({
        "subject": email.subject,
        "body": email.body,
        "user_id": professor["google_id"],
        "category": "",
        "retrieved_context": "",
        "decision": "",
        "draft_reply": ""
    })

    if result["draft_reply"]:
        return {
            "status": "auto-replied",
            "category": result["category"],
            "reply": result["draft_reply"]
        }
    else:
        return {
            "status": "escalated",
            "category": result["category"],
            "reply": None
        }
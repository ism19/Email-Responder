from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph import agent

router = APIRouter()

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str
    user_id: str

@router.post("/process-email")
async def process_email(email: EmailInput):
    result = agent.invoke({
        "subject": email.subject,
        "body": email.body,
        "user_id": email.user_id,
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
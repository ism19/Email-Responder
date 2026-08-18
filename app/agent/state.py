from typing import TypedDict

class EmailState(TypedDict):
    subject: str
    body: str
    user_id: str
    category: str
    retrieved_context: str
    decision: str
    draft_reply: str
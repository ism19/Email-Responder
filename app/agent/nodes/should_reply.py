from state import EmailState
from typing import Literal

def should_reply(state: EmailState) -> Literal["draft_reply", "escalate"]:
    if state["decision"] == "answerable":
        return "draft_reply"
    return "escalate"
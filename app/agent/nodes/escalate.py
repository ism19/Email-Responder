from state import EmailState

def escalate(state: EmailState) -> EmailState:
    return {**state, "draft_reply": ""}
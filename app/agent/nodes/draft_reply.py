from state import EmailState
from chains.reply_drafter import reply_drafter

def draft_reply(state: EmailState) -> EmailState:
    draft = reply_drafter.invoke({"subject": state["subject"], "body": state["body"], "retrieved_context": state["retrieved_context"]})
    return {**state, "draft_reply": draft.content}
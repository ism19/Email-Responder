from state import EmailState
from typing import Literal

def should_lookup(state: EmailState) -> Literal["rag_lookup", "escalate", "__end__"]:
    if state["category"] == "syllabus_question":
        return "rag_lookup"
    if state["category"] == "spam":
        return "__end__"
    return "escalate"
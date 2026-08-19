from state import EmailState
from typing import Literal

def should_lookup(state: EmailState) -> Literal["rag_lookup", "escalate", "__end__"]:
    if state["category"] == "student":
        return "rag_lookup"
    if state["category"] == "irrelevant":
        return "__end__"
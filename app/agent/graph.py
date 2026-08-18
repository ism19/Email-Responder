from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from state import EmailState
from nodes import classify_email, rag_lookup, make_decision, draft_reply, escalate, should_reply, should_lookup

load_dotenv()

graph = StateGraph(EmailState)

graph.add_node("classify_email", classify_email)
graph.add_node("rag_lookup", rag_lookup)
graph.add_node("make_decision", make_decision)
graph.add_node("draft_reply", draft_reply)
graph.add_node("escalate", escalate)

graph.set_entry_point("classify_email")
graph.add_conditional_edges("classify_email", should_lookup)
graph.add_edge("rag_lookup", "make_decision")
graph.add_conditional_edges("make_decision", should_reply)
graph.add_edge("draft_reply", END)
graph.add_edge("escalate", END)

agent = graph.compile()
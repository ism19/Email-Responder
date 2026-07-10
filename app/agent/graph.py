import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.rag.retriever import retrieve

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class EmailState(TypedDict):
    subject: str
    body: str
    user_id: str
    category: str
    retrieved_context: str
    decision: str
    draft_reply: str

def classify_email(state: EmailState) -> EmailState:
    prompt = f"""
    Classify this student email into one of the following categories:
    - syllabus_question: can be answered from course syllabus (policies,
      deadlines, grading, course schedule)
    - admin: assignment and project extensions, accomodations, scheduling,
      grade disputes, extenuating circumstances
    - spam: irrelevant or junk

    Subject: {state['subject']}
    Body: {state['body']}

    Always check if it's possibly a syllabus question first. Respond with
    ONLY the category name from the options (syllabus_question, admin, spam).
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "category": response.content.strip().lower()}

def should_lookup(state: EmailState) -> Literal["rag_lookup", "escalate"]:
    if state["category"] == "syllabus_question":
        return "rag_lookup"
    return "escalate"

def rag_lookup(state: EmailState) -> EmailState:
    query = f"{state['subject']} {state['user_id']}"
    context = retrieve(query=query, user_id=state["user_id"])
    return {**state, "retrieved_context": context}

def make_decision(state: EmailState) -> EmailState:
    prompt = f"""
    You are an email assistant helping a professor manage student emails.

    Student email: 
    Subject: {state['subject']}
    Body: {state['body']}

    Syllabus content retrieved:
    {state['retrieved_context']}

    Can this email be answered correctly and completely with sufficient 
    information from the content retrieved from the syllabus. Respond with
    ONLY "answerable" OR "escalate"
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "decision": response.content}

def should_reply(state: EmailState) -> Literal["draft_reply", "escalate"]:
    if state["decision"] == "answerable":
        return "draft_reply"
    return "escalate"

def draft_reply(state: EmailState) -> EmailState:
    prompt = f"""
    You are a helpful professor's assistant answering common questions
    from students. Write a professional reply to this student's email 
    using ONLY the information provided in the syllabus content provided
    below. DO NOT make up or assume anything that isn't stated in the 
    provided content. Maintain a friendly tone and open the email with 
    "Hello, (student name)." if their name is included in the student email.

    Student email:
    Subject: {state['subject']}
    Body: {state['body']}

    Relevant syllabus content:
    {state['retrieved_context']}

    Write only the body of the email.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "draft_reply": response.content}

def escalate(state: EmailState) -> EmailState:
    return {**state, "draft_reply": ""}

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
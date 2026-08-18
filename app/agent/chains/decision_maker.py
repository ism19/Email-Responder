from enum import Enum
from state import EmailState
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class DecisionType(str, Enum): 
    answerable = "answerable"
    escalate = "escalate"

class Decision(BaseModel):
    decision: DecisionType = Field(description="Decision type")
    reasoning: str = Field(description="Brief justification for descion made")

llm = ChatOpenAI(temperature=0, model="gpt-4o")

structured_llm = llm.with_structured_output(Decision)

system = """
    You are an email assistant helping a professor manage student emails.
    Your job is to examine an email's subject, body, and the syllabus content
    given to you and judge whether the syllabus content can sufficiently 
    answer the email correctly and completely. You can either espond with
    "answerable" OR "escalate".
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    (
        "human",
        """
            Student email: 
            Subject: {subject}
            Body: {body}

            Syllabus content retrieved:
            {retrieved_context}
        """
    )
])

decision_maker = prompt | structured_llm

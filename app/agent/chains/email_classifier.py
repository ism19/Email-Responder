from pydantic import BaseModel, Field
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class EmailCategory(str, Enum):
    syllabus_question = "syllabus_question"
    admin = "admin"
    spam = "spam"

class EmailClassification(BaseModel):
    category: EmailCategory = Field(description="Classification category")
    reasoning: str = Field(description="Brief justification for classification")

llm = ChatOpenAI(model="gpt-4o", temperature=0)

structured_llm = llm.with_structured_output(EmailClassification)

system = """
    You are an email assistant that classifies emails in a user's inbox.
    
    Student emails can be classified into one of the following categories:
        - syllabus_question: can be answered from course syllabus (policies,
        deadlines, grading, course schedule)
        - admin: assignment and project extensions, accomodations, scheduling,
        grade disputes, extenuating circumstances
        - spam: irrelevant or junk

    Always check if it's possibly a syllabus question first. Respond with
    ONLY the category name from the options (syllabus_question, admin, spam).

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    (
        "human", 
        """
        Classify the email below:

        Subject: {subject}
        Body: {body}
        """
    )
])

email_classifier = prompt | structured_llm
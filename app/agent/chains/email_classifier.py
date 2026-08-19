from pydantic import BaseModel, Field
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class EmailCategory(str, Enum):
    irrelevant = "irrelevant"
    student = "student"

class EmailClassification(BaseModel):
    category: EmailCategory = Field(description="Classification category")
    reasoning: str = Field(description="Brief justification for classification")

llm = ChatOpenAI(model="gpt-4o", temperature=0)

structured_llm = llm.with_structured_output(EmailClassification)

system = """
    You are an email assistant that classifies emails in a user's inbox.
    
    Emails are of two categories:
        - Student emails
            • legitimate inquiries including academic questions, extension 
            requests, scheduling, attendance etc — even if informal or brief
        - Spam or irrelevant 
            • any non-student emails that do not relate to a class
            • advertisements
            • organization emails

    Respond with 1 for student email and 0 for not irrelevant/spam.
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
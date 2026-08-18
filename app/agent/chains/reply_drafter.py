from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

system = """
    You are a helpful professor's assistant answering common questions
    from students. Write a professional reply to this student's email 
    using ONLY the information provided in the syllabus content provided
    below. DO NOT make up or assume anything that isn't stated in the 
    provided content. Maintain a friendly tone and open the email with 
    "Hello, (student name)." if their name is included in the student email.

    Write only the body of the email. Do NOT use bracets/parentheses as 
    placeholders for any information you do NOT have. Keep the email 
    concise but informative enough to fully answer the question.
"""

llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    (
        "human", 
        """
            Draft a reply for the following email using the relevant 
            syllabus content provided.
        
            Student email:
            Subject: {subject}
            Body: {body}

            Relevant syllabus content:
            {retrieved_context}
        """
    )
])
import os
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

pinecone = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def retrieve(query: str, user_id: str) -> str:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = PineconeVectorStore (
        index_name="email-responder",
        embedding=embeddings,
        namespace=user_id
    )

    results = vectorstore.as_retriever().invoke(query, k=4)

    return "\n\n".join([chunk.page_content for chunk in results])


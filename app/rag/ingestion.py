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
index = pinecone.Index("email-responder")

def ingest_syllabus(pdf: bytes, user_id: str):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
        temp.write(pdf)
        temp_path = temp.name

    loader = PyPDFLoader(temp_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    PineconeVectorStore.from_documents (
        documents=chunks,
        embedding=embeddings,
        index_name="email-responder",
        namespace=user_id
    )

    os.remove(temp_path)



    
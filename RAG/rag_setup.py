from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

docs=[]

for file in os.listdir("manual"):
    if file.endswith(".pdf"):
        loader=PyPDFLoader(os.path.join("manual",file))
        doc=loader.load()
        docs.extend(doc)

splitter=RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunk=splitter.split_documents(docs)

embeddings=HuggingFaceEmbeddings(
    model="all-MiniLM-L6-v2"
)

vd=FAISS.from_documents(chunk,embeddings)

vd.save_local("vector_store")

print("FAISS vector db created successfully!")

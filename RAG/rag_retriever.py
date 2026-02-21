from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings=HuggingFaceEmbeddings(
    model="all-MiniLM-L6-v2"
)

vd=FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

ret=vd.as_retriever(search_kwargs={"k":3})

def get_context(query):
    docs=ret.invoke(query)
    return "\n".join([doc.page_content for doc in docs])

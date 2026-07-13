
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
def create_vectorstore(chunks):

    print(f"Total chunks: {len(chunks)}")

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vectorstore.save_local("faiss_index")

    return vectorstore

def load_vectorstore():
    """
    Loads the saved FAISS vector database.
    """
    vectorstore = FAISS.load_local(
    "faiss_index",
    get_embeddings(),
    allow_dangerous_deserialization=True
)
    return vectorstore

def get_retriever(vectorstore):
    """
    Creates a retriever from the vector database.
    """

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
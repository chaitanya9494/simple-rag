from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def create_vector_store(chunks: list[Document], embeddings: Embeddings) -> FAISS:
    if not chunks:
        raise ValueError("There are no chunks to index.")
    return FAISS.from_documents(chunks, embeddings)


def retrieve(question: str, vector_store: FAISS, k: int = 4) -> list[Document]:
    if not question.strip():
        raise ValueError("Enter a question.")
    if k < 1:
        raise ValueError("Retrieve at least one chunk.")
    return vector_store.similarity_search(question.strip(), k=k)

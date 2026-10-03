from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document], chunk_size: int = 1000,
                    chunk_overlap: int = 200) -> list[Document]:
    if chunk_size <= 0 or not 0 <= chunk_overlap < chunk_size:
        raise ValueError("Overlap must be nonnegative and smaller than chunk size.")
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap,
        add_start_index=True,
    ).split_documents(documents)

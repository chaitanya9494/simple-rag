import os

from langchain_openai import OpenAIEmbeddings


def create_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        request_timeout=30, max_retries=2,
    )

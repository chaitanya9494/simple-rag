from pathlib import Path

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from rag.chunker import split_documents
from rag.generator import ModelAnswer, generate
from rag.loader import load_pdf
from rag.retriever import create_vector_store, retrieve

SAMPLE = Path(__file__).resolve().parents[1] / "sample_docs" / "acme-policy.pdf"


class TopicEmbeddings(Embeddings):
    """Deterministic vectors test wiring, not real embedding quality."""
    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        return [float("refund policy" in text.lower()), float("support" in text.lower()), 0.1]


class StubModel:
    def __init__(self, ids):
        self.ids = ids

    def invoke(self, messages):
        assert "PDF page 3" in messages[1][1]
        return ModelAnswer(answer="Within 30 days of the first purchase.", source_ids=self.ids)


def test_pdf_to_retrieval_preserves_source_pages():
    documents = load_pdf(SAMPLE.read_bytes(), SAMPLE.name)
    assert [d.metadata["page"] for d in documents] == [1, 2, 3, 4]
    chunks = split_documents(documents, chunk_size=250, chunk_overlap=30)
    assert len(chunks) > len(documents)
    store = create_vector_store(chunks, TopicEmbeddings())
    result = retrieve("refund policy", store, k=1)
    assert result[0].metadata["page"] == 3
    assert result[0].metadata["source"] == SAMPLE.name


@pytest.mark.parametrize("ids", [[], [0], [2], [1, 99]])
def test_missing_or_invalid_citations_fail_closed(ids):
    context = [Document(page_content="Refunds within 30 days", metadata={"page": 3})]
    result = generate("Refund policy?", context, StubModel(ids))
    assert not result.sources
    assert "supported answer" in result.text


def test_valid_citations_are_deduplicated():
    doc = Document(page_content="Refunds within 30 days", metadata={"page": 3})
    result = generate("Refund policy?", [doc], StubModel([1, 1]))
    assert result.sources == [doc]
    assert "30 days" in result.text


def test_empty_context_does_not_call_model():
    assert generate("Unknown?", [], object()).sources == []


def test_invalid_inputs():
    with pytest.raises(ValueError):
        split_documents([], 100, 100)
    with pytest.raises(ValueError):
        create_vector_store([], TopicEmbeddings())
    with pytest.raises(ValueError):
        retrieve(" ", None)

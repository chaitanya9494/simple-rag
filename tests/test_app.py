from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_app_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app = AppTest.from_file(APP).run(timeout=30)
    assert not app.exception
    assert app.title[0].value == "Ask Your PDF"
    assert "OPENAI_API_KEY" in app.info[0].value


def test_index_ask_and_change_document(monkeypatch):
    from langchain_core.documents import Document
    from rag.generator import Answer
    import rag.embeddings
    import rag.generator
    import rag.retriever

    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-real")
    monkeypatch.setattr(rag.embeddings, "create_embeddings", lambda: object())
    monkeypatch.setattr(rag.retriever, "create_vector_store", lambda chunks, embeddings: object())
    evidence = Document(page_content="Refunds within 30 days.",
                        metadata={"page": 3, "source": "acme-policy.pdf"})
    monkeypatch.setattr(rag.retriever, "retrieve", lambda *args: [evidence])
    monkeypatch.setattr(rag.generator, "generate", lambda *args: Answer("Within 30 days.", [evidence]))
    app = AppTest.from_file(APP).run(timeout=30)
    next(b for b in app.button if b.label == "Build PDF index").click().run()
    assert not app.exception
    assert "Indexed 4 text pages" in app.success[0].value
    app.text_input[0].input("What is the refund policy?")
    next(b for b in app.button if b.label == "Ask").click().run()
    assert not app.exception
    assert any("Cited PDF pages: 3" in c.value for c in app.caption)
    app.checkbox[0].uncheck().run()
    with pytest.raises(KeyError):
        app.session_state["index"]

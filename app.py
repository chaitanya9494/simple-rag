"""Run with: streamlit run app.py"""
import hashlib
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag.chunker import split_documents
from rag.embeddings import create_embeddings
from rag.generator import generate
from rag.loader import load_pdf
from rag.retriever import create_vector_store, retrieve

load_dotenv()
st.set_page_config(page_title="Ask Your PDF", page_icon="📄")
st.title("Ask Your PDF")
st.caption("Minimal RAG for Software Engineers · by Amal Chaitanya")
st.markdown("Upload a PDF, ask a question, and inspect the pages behind the answer.")

with st.sidebar:
    st.header("How it works")
    st.markdown("PDF → chunks → embeddings → FAISS\n\nQuestion → retrieval → LLM → answer + sources")
    st.caption("PDF text and questions are sent to OpenAI. API usage may incur charges.")
    sample = st.checkbox("Use the sample policy PDF", value=True)
    k = st.slider("Chunks to retrieve", 1, 8, 4)
    if st.button("Clear session"):
        st.session_state.clear()
        st.rerun()

uploaded = None if sample else st.file_uploader("Upload PDF (up to 10 MB)", type=["pdf"])
if sample:
    path = Path(__file__).parent / "sample_docs" / "acme-policy.pdf"
    data, filename = path.read_bytes(), path.name
    st.download_button("Download sample PDF", data, filename, "application/pdf")
elif uploaded:
    data, filename = uploaded.getvalue(), uploaded.name
else:
    for name in ("index", "result", "retrieved", "stats", "document_key"):
        st.session_state.pop(name, None)
    st.info("Choose a PDF to begin.")
    st.stop()

if len(data) > 10 * 1024 * 1024:
    st.error("Choose a PDF smaller than 10 MB.")
    st.stop()

key = hashlib.sha256(data).hexdigest() + filename + os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
# State is per browser session. Never share uploaded documents through a global cache.
if st.session_state.get("document_key") != key:
    for name in ("index", "result", "retrieved", "stats", "document_key"):
        st.session_state.pop(name, None)

if not os.getenv("OPENAI_API_KEY"):
    st.info("Add OPENAI_API_KEY to your .env file, then restart Streamlit.")
    st.stop()

if st.button("Build PDF index", disabled="index" in st.session_state, type="primary"):
    try:
        with st.spinner("Extracting, chunking, and embedding your PDF…"):
            documents = load_pdf(data, filename)
            chunks = split_documents(documents)
            if len(chunks) > 500:
                raise ValueError("This teaching demo supports up to 500 chunks. Use a smaller PDF.")
            vector_store = create_vector_store(chunks, create_embeddings())
            st.session_state.update(index=vector_store, document_key=key,
                                    stats=(len(documents), len(chunks)))
        st.rerun()
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error("Indexing failed. Check the PDF, API key, network, and API quota, then retry.")

if "index" not in st.session_state:
    st.stop()

pages, chunks_count = st.session_state.stats
st.success(f"Indexed {pages} text pages into {chunks_count} chunks.")
with st.form("question"):
    question = st.text_input("Question", placeholder="What is the refund policy?")
    submitted = st.form_submit_button("Ask", type="primary")
if submitted:
    st.session_state.pop("result", None)
    st.session_state.pop("retrieved", None)
    if not question.strip():
        st.warning("Enter a question.")
    else:
        try:
            with st.spinner("Retrieving passages and generating an answer…"):
                context = retrieve(question, st.session_state.index, k)
                result = generate(question, context)
                st.session_state.update(result=result, retrieved=context)
        except Exception:
            st.error("The request failed. Check your API key, network, and quota, then retry.")

if "result" in st.session_state:
    result = st.session_state.result
    st.subheader("Answer")
    st.write(result.text)
    if result.sources:
        pages = sorted({doc.metadata["page"] for doc in result.sources})
        st.caption("Cited PDF pages: " + ", ".join(map(str, pages)))
        st.subheader("Sources")
        for i, doc in enumerate(result.sources, start=1):
            with st.expander(f"Source {i} · {doc.metadata['source']} · page {doc.metadata['page']}"):
                st.text(doc.page_content)
    with st.expander("Inspect all retrieved chunks"):
        for i, doc in enumerate(st.session_state.retrieved, start=1):
            st.markdown(f"**Chunk {i} · PDF page {doc.metadata['page']}**")
            st.text(doc.page_content)
    st.caption("Citations identify retrieved evidence; they do not guarantee the answer is correct.")

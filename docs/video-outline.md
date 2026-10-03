# Ask Your PDF — six-minute recording outline

## 0:00–0:20 — opening, on camera

“Your language model knows a lot, but it doesn't automatically know what's in your PDF. Today we'll build a small app that retrieves the relevant passages, gives them to a model, and shows the sources behind its answer.”

## 0:20–1:00 — slide 1: What problem does RAG solve?

Slide text:

- LLM: general knowledge
- Your private documents, internal data, and recent information need context
- Retrieve relevant information at question time

Say: “We don't need to retrain the model for this demo. We retrieve relevant information and put it into the prompt.”

## 1:00–2:30 — slide 2: How RAG works

Use the architecture diagram from the README. Show indexing first, then the query path.

“We extract PDF text page by page and split it into small overlapping chunks. An embedding turns each chunk into a vector. FAISS stores these vectors for similarity search. When we ask a question, we embed it too, retrieve nearby chunks, and send those chunks with the question to the LLM.”

“The model is still generating the answer. Retrieval chooses what evidence it gets to see.”

## 2:30–4:30 — live demo

Before recording: install dependencies, configure `.env`, run Streamlit, check API quota, and keep the fictional sample selected. Avoid showing credentials on screen.

1. Show the sample PDF; point to the refund policy on page 3.
2. Click **Build PDF index**. Explain the page and chunk counts.
3. Ask “What is the refund policy?”
4. Expand a cited passage. Compare the answer with the actual text.
5. Expand **Inspect all retrieved chunks**. Explain that retrieved evidence and cited evidence can differ.
6. Ask “What is the CEO's favorite programming language?” Show the abstention if it occurs. If the model invents an answer, explain honestly that basic RAG still needs evaluation.

Say: “These citations let us inspect where an answer came from. They don't automatically prove every claim is correct.”

## 4:30–5:30 — code walkthrough

Show the five-step code snippet in the README, then these two details:

- `rag/loader.py`: page metadata follows the text into chunks.
- `rag/generator.py`: structured source IDs are checked against retrieved chunks.

Avoid reading every line. “Each file has one job. You can follow the entire pipeline without a large framework abstraction.”

## 5:30–6:00 — slide 3: RAG is more than calling an LLM

Slide text:

- Chunking
- Embeddings
- Retrieval and ranking
- Prompt and context
- Evaluation

“A useful answer depends on retrieving useful evidence. Next we'll change the chunk size and see what happens. The project is open source; the GitHub link is in the description.”

## Description text

Build a minimal PDF RAG app with Python, LangChain, FAISS, OpenAI, and Streamlit. Learn ingestion, chunking, embeddings, similarity search, generation, and source citations.

Code: https://github.com/chaitanya9494/simple-rag

This is a local educational demo. API usage can incur charges. Use fictional or approved documents because extracted text is sent to the model provider.

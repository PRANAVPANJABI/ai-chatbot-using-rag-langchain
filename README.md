# AI PDF Chatbot using LangChain & RAG

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-orange)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-blue)

A beginner-friendly AI-powered PDF Question Answering application built with **Python**, **LangChain**, **Google Gemini**, **FAISS**, **Hugging Face Embeddings**, and **Streamlit**.

A document question-answering system that lets users upload one or more PDFs and query them in natural language. Built with a RAG pipeline so that answers are grounded in retrieved document content rather than the full text of the file.

## Overview

Reading an entire PDF for every question is inefficient, especially for larger documents. This project first searches for the most relevant parts of the document and then uses only those sections to answer the user's question. This approach improves speed, reduces unnecessary processing, and keeps responses focused on the uploaded content.

## Architecture

```text
Upload PDF(s)
      │
      ▼
Extract text (PyPDF)
      │
      ▼
Split into chunks
      │
      ▼
Create vector representations (Hugging Face)
      │
      ▼
Store in FAISS index
      │
      ▼
User question → similarity search
      │
      ▼
Relevant text + question → Google Gemini API
      │
      ▼
Answer
```

The system is split into three modules rather than a single script:

- `pdf_processor.py` — text extraction and chunking
- `vector_store.py` — embedding generation and FAISS index management
- `chatbot.py` — retrieval and language model query workflow

## Tech Stack

| Component | Choice |
|---|---|
| language model | Google Gemini API |
| Orchestration | LangChain |
| Vector representations | Hugging Face sentence vector representations |
| Vector store | FAISS |
| PDF parsing | PyPDF |
| Interface | Streamlit |
| Config | python-dotenv |

## Design Decisions

**Using only relevant sections instead of the entire document.** Sending the full PDF on every query doesn't scale past a few pages and increases the surface area for incorrect responses. Retrieving only the top-matching chunks keeps the context focused and reduces token usage per query.

**Why FAISS?** FAISS is lightweight, runs locally, and is a good fit for this desktop project. For larger applications with multiple users, a managed vector database would be a better choice.

**Organized project structure.** Separating PDF processing, vector storage, and chat workflow into distinct modules keeps each concern independently testable and makes it straightforward to swap components (e.g. a different embedding model or vector store) without touching the rest of the pipeline.

## Setup

```bash
git clone https://github.com/PRANAVPANJABI/ai-chatbot-using-rag-langchain.git
cd ai-chatbot-using-rag-langchain

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run the app:

```bash
streamlit run app.py
```

## Usage

1. Upload one or more PDF files through the Streamlit interface.
2. Wait for text extraction, chunking, and index creation to complete.
3. Ask a question in natural language.
4. The system retrieves the most relevant chunks and returns a Gemini-generated answer grounded in that context.
5. With multiple PDFs uploaded, queries can be answered across documents.

## Known Limitations

- No conversation memory — each query is handled independently of prior turns.
- No source attribution in the UI — retrieved chunks aren't surfaced alongside the answer.
- Retrieval is single-strategy (dense vector similarity); no hybrid keyword + semantic search.
- Local-only; not yet deployed or multi-user.
- Limited to PDF input; no support for Word, TXT, or PPT documents.

## Screenshots

See `assets/screenshots/` for the upload flow, processing state, and example single- and multi-document Q&A sessions.

## Author

**Pranavkumar Panjabi**
[GitHub](https://github.com/PRANAVPANJABI) · [LinkedIn](https://www.linkedin.com/in/pranavkumar-panjabi)

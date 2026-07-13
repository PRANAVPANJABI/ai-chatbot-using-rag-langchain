# Imports and Setup

import os
import hashlib

import streamlit as st
from dotenv import load_dotenv
from google import genai

from utils.pdf_processor import process_pdfs
from utils.vector_store import (
    create_vectorstore,
    get_retriever,
)
from utils.chatbot import ask_pdf


def calculate_files_hash(uploaded_files):
    """
    Returns a SHA-256 hash for all uploaded PDF files.
    """

    hash_object = hashlib.sha256()

    for uploaded_file in uploaded_files:
        hash_object.update(uploaded_file.getvalue())

    return hash_object.hexdigest()


# Load Environment Variables

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API Key not found.")
    st.stop()


# Initialize Gemini Client

if "client" not in st.session_state:
    st.session_state.client = genai.Client(
        api_key=api_key
    )


# Initialize Session State

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "current_pdf_hash" not in st.session_state:
    st.session_state.current_pdf_hash = None

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False


# User Interface

st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI PDF Chatbot using LangChain & RAG")

st.write(
    "Upload one or more PDFs and ask questions about their content."
)

st.divider()


# Upload and Process PDFs

uploaded_files = st.file_uploader(
    "📄 Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:

    current_hash = calculate_files_hash(uploaded_files)

    if current_hash != st.session_state.current_pdf_hash:

        pdf_paths = []

        for uploaded_file in uploaded_files:

            pdf_path = os.path.join(
                "pdfs",
                uploaded_file.name,
            )

            with open(pdf_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            pdf_paths.append(pdf_path)

        try:

            with st.spinner(
                "⏳ Uploading and processing PDF(s)..."
            ):

                chunks = process_pdfs(pdf_paths)

                vectorstore = create_vectorstore(chunks)

                retriever = get_retriever(vectorstore)

            st.session_state.vectorstore = vectorstore
            st.session_state.retriever = retriever
            st.session_state.current_pdf_hash = current_hash
            st.session_state.pdf_ready = True

            st.success(
                "✅ PDF(s) processed successfully! You can now ask questions."
            )

        except Exception as e:

            st.error(
                "❌ Failed to process the uploaded PDF(s)."
            )

            st.exception(e)

            st.stop()


# Ask Questions

if st.session_state.pdf_ready:

    with st.form("chat_form"):

        question = st.text_input(
            "💬 Ask a question about your PDF"
        )

        submitted = st.form_submit_button("Ask")

    if submitted and question.strip():

        with st.spinner("🤖 Thinking..."):

            answer = ask_pdf(
                question,
                st.session_state.retriever,
                st.session_state.client,
            )

        st.markdown("### 🤖 Answer")

        st.info(answer)
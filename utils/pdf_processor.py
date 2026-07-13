from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_pdfs(pdf_paths):
    """
    Reads multiple PDF files,
    splits them into text chunks,
    and returns the chunked documents.
    """

    all_documents = []

    # Read all uploaded PDFs
    for pdf_path in pdf_paths:

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

        all_documents.extend(documents)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        all_documents
    )

    return chunks
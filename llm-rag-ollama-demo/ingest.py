# ingest.py
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


DATA_DIR = "data"
VECTOR_DIR = "vectordb"
MODEL_NAME = "llama3"  # Ollama model name, for embedding


def load_documents():
    docs = []

    # 1) Markdown
    text_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True,
    )
    docs.extend(text_loader.load())

    txt_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True,
    )
    docs.extend(txt_loader.load())

    # 2) PDF
    pdf_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True,
    )
    docs.extend(pdf_loader.load())

    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
    )
    return splitter.split_documents(docs)


def build_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DIR,
    )
    vectordb.persist()
    return vectordb


def main():
    print("📥 Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")

    print("✂️ Splitting documents...")
    chunks = split_documents(docs)
    print(f"Got {len(chunks)} chunks.")

    print("🧠 Building vector store...")
    build_vectorstore(chunks)
    print("✅ Vector store built and persisted.")


if __name__ == "__main__":
    main()

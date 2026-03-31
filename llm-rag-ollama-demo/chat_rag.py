"""
chat_rag.py：RAG Question-Answer main route
"""
# chat_rag.py
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


VECTOR_DIR = "vectordb"
EMBED_MODEL = "llama3"
LLM_MODEL = "llama3"


def get_vectorstore():
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR,
    )
    return vectordb


def get_llm():
    return Ollama(
        model=LLM_MODEL,
        temperature=0.2,
    )


def build_rag_chain():
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = get_llm()

    template = """
You are a helpful assistant using Retrieval-Augmented Generation (RAG).
You must answer the user's question **only** based on the provided context.
If the context is insufficient, say you don't know and suggest what additional info is needed.

Context:
{context}

Question:
{question}

Answer in clear, concise English, structured if helpful.
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"],
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return qa


def main():
    qa = build_rag_chain()
    print("✅ RAG chat ready. Type your question (q to quit).")

    while True:
        query = input("\nYou: ").strip()
        if query.lower() in ["q", "quit", "exit"]:
            print("Bye.")
            break

        result = qa({"query": query})
        answer = result["result"]
        sources = result["source_documents"]

        print("\nAssistant:\n", answer)
        print("\n--- Sources ---")
        for i, doc in enumerate(sources, 1):
            print(f"[{i}] {doc.metadata.get('source', 'unknown')}")


if __name__ == "__main__":
    main()

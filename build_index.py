from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def build_vector_store():
    print("Loading .md documents...")
    md_loader = DirectoryLoader(
        "knowledge_base",
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True
    )
    md_docs = md_loader.load()
    print(f"Loaded {len(md_docs)} markdown files")

    print("Loading PDF documents...")
    pdf_loader = DirectoryLoader(
        "knowledge_base",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    pdf_docs = pdf_loader.load()
    print(f"Loaded {len(pdf_docs)} PDF pages")

    all_docs = md_docs + pdf_docs
    print(f"Total: {len(all_docs)} documents")

    print("Splitting...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and storing...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=os.getenv("CHROMA_DB_PATH")
    )
    print(f"Vector store saved to {os.getenv('CHROMA_DB_PATH')}")
    print(f"Total chunks stored: {vectordb._collection.count()}")
    return vectordb

if __name__ == "__main__":
    build_vector_store()
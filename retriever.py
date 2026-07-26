import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def load_vector_store() -> Chroma:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectorstore = Chroma(
        persist_directory=os.getenv("CHROMA_DB_PATH"),   # ./chroma_db from .env
        embedding_function=embeddings
    )
    print(f"Loaded ChromaDB from {os.getenv('CHROMA_DB_PATH')} "
          f"— {vectorstore._collection.count()} chunks")
    return vectorstore

if __name__ == "__main__":
    vs = load_vector_store()
    # Should print the number of chunks you built (e.g. 10 from build_index.py)

from langchain_core.vectorstores import VectorStoreRetriever

def build_retriever(vectorstore: Chroma) -> VectorStoreRetriever:
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,           # final chunks returned to agent
            "fetch_k": 20,    # MMR candidate pool
            "lambda_mult": 0.7
        }
    )

if __name__ == "__main__":
    vs = load_vector_store()
    retriever = build_retriever(vs)
    results = retriever.invoke("What is AVE and how is it interpreted?")
    for doc in results:
        print(doc.metadata.get("source"), "—", doc.page_content[:120])
        print("---")
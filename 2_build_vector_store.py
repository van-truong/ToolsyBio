### 2_build_vector_store.py
"""
This script builds the vector store from bio.tools data.
Run this once before using the RAG system.
"""
import json
import os
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration
JSON_DATA_PATH = "data/biotools_data.json"
CHUNK_SIZE = 1000 # Size of each chunk
CHUNK_OVERLAP = 100 # Overlap between chunks
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" 
PERSIST_DIRECTORY = "chroma_db"


def load_and_split_documents():
    with open(JSON_DATA_PATH, 'r') as f:
        data = json.load(f)

    documents = [
        Document(
            page_content=item["text_content"],
            metadata={"id": item["id"], "name": item["name"], "source": item["source"]}
        ) for item in data
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def create_and_store_embeddings(chunks):
    print(f"🔍 Creating embeddings for {len(chunks)} chunks...")
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Use tqdm to visually track embedding creation
    vector_store = Chroma.from_documents(
        documents=tqdm(chunks, desc="🔢 Embedding Chunks"),
        embedding=embeddings_model,
        persist_directory=PERSIST_DIRECTORY
    )
    print("📦 Vector store created at:", PERSIST_DIRECTORY)

if __name__ == "__main__":
    print("Building vector database...")
    chunks = load_and_split_documents()
    create_and_store_embeddings(chunks)
    print("✅ Vector database build complete.")

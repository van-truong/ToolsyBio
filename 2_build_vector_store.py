### 2_build_vector_store.py
# --------------------------------------------
# This script builds a Chroma vector store from tool metadata
# previously saved in data/biotools_data.json.
#
# It splits each tool description into chunks, generates embeddings,
# and stores them locally for use in the RAG system.
# --------------------------------------------

import json
import os
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings

# --- Configuration ---
JSON_DATA_PATH = "data/biotools_data.json"       # Path to metadata JSON (from 1_fetch_biotools.py)
PERSIST_DIRECTORY = "chroma_db"                  # Where the vector store will be saved
CHUNK_SIZE = 1000                                 # Max characters per chunk
CHUNK_OVERLAP = 100                               # Characters of overlap between chunks
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"         # SentenceTransformer model


def load_and_split_documents():
    """
    Loads the saved JSON tool data and splits each tool into overlapping text chunks.
    """
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
    """
    Embeds the document chunks and saves them to a persistent Chroma vector store.
    """
    print(f"🔍 Creating embeddings for {len(chunks)} chunks...")
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Use tqdm to visually track embedding creation
    vector_store = Chroma.from_documents(
        documents=tqdm(chunks, desc="🔢 Embedding Chunks"),
        embedding=embeddings_model,
        persist_directory=PERSIST_DIRECTORY
    )
    print("📦 Vector store created at:", PERSIST_DIRECTORY)

# --- Entry Point ---
if __name__ == "__main__":
    print("Building vector database...")
    chunks = load_and_split_documents()
    create_and_store_embeddings(chunks)
    print("✅ Vector database build complete.")

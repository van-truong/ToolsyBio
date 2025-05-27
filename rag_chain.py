### rag_chain.py
# --------------------------------------------
# This module sets up the Retrieval-Augmented Generation (RAG) chain
# used by ToolsyBio. It loads the Chroma vector store, builds a retriever,
# connects to a local LLM served by Ollama, and defines the prompt pipeline.
#
# Used by both the Streamlit frontend and batch/CLI interfaces.
# --------------------------------------------

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Embedding model used for vector store
PERSIST_DIRECTORY = "chroma_db"            # Folder where ChromaDB is stored
OLLAMA_MODEL = "mistral"                   # Local LLM name served by Ollama

def load_vector_store():
    """
    Loads the Chroma vector store from disk and initializes the embedding function.
    """
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings_model)

def format_docs(docs):
    """
    Formats retrieved documents into Markdown with hyperlinks to their source metadata.
    """
    return "\n\n---\n\n".join([
        f"Source: [{doc.metadata.get('name')}]({doc.metadata.get('source')})\n\n{doc.page_content}"
        for doc in docs
    ])

def setup_rag_chain(vector_store, k=3):
    """
    Builds the RAG chain using the provided vector store and top-k retrieval parameter.
    
    Parameters:
        vector_store: A Chroma vector store already loaded.
        k (int): Number of top matching chunks to retrieve for each query.

    Returns:
        chain: LangChain pipeline for answering questions
        retriever: Configured retriever for direct use
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    llm = Ollama(model=OLLAMA_MODEL)

    # Prompt template for LLM: grounded context + user query
    template = """
    You are an assistant for answering questions about bioinformatics software tools.
    Use the following pieces of context to answer the question.
    Be concise. If a homepage or documentation is mentioned, include it.

    Context:
    {context}

    Question: {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever
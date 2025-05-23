### rag_chain.py
"""
This module loads the vector DB and sets up the RAG chain.
It’s used by both CLI or Streamlit interfaces.
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configuration
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "chroma_db"
OLLAMA_MODEL = "mistral"

def load_vector_store():
    # Set up the vector store for Chroma
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings_model)

# Format retrieved docs as Markdown strings with source names
def format_docs(docs):
    return "\n\n---\n\n".join([
        f"Source: [{doc.metadata.get('name')}]({doc.metadata.get('source')})\n\n{doc.page_content}"
        for doc in docs
    ])

def setup_rag_chain(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model=OLLAMA_MODEL)

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

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    ), retriever
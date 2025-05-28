### 3_run_streamlit_app.py
# --------------------------------------------
# This script launches the Streamlit front end for ToolsyBio.
# Users can ask natural language questions about bioinformatics tools.
# The system uses a local vector store + Ollama LLM for RAG-based answers.
# --------------------------------------------

import streamlit as st
from rag_chain import load_vector_store, setup_rag_chain
from eval_logger import log_evaluation

# --- Page setup ---
st.set_page_config(page_title="ToolsyBio - RAG Demo", layout="wide")
st.title("🔬 ToolsyBio: Bioinformatics Tool Advisor")
st.markdown("""
Ask any question about bioinformatics software tools indexed in `bio.tools`.

Powered by a local large language model via [Ollama](https://ollama.com/) and semantic search using ChromaDB + LangChain.
""")


# --- Load RAG pipeline only once (cached) ---
@st.cache_resource
def get_rag():
    """
    Initializes the RAG chain and vector retriever (cached across reloads).
    """
    vs = load_vector_store()
    chain, retriever = setup_rag_chain(vs)
    return chain, retriever

chain, retriever = get_rag()

# --- Main interaction UI ---
query = st.text_input("🔍 Ask a question:", placeholder="e.g. What tools do differential expression analysis?")
if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        try:
            # Step 1: Retrieve relevant documents from vector store
            docs = retriever.get_relevant_documents(query)

            # Step 2: Format sources for display
            formatted_context = "\n\n".join([f"**{d.metadata['name']}** — [source]({d.metadata['source']})" for d in docs])
            
            # Step 3: Get LLM-generated answer
            response = chain.invoke(query)

            # Step 4: Display response and sources
            st.subheader("💡 Answer")
            st.markdown(response)
            st.markdown("---")
            st.subheader("📚 Top Sources")
            st.caption("_These are the top tools retrieved based on your query. Not all may appear in the final answer._")
            st.markdown(formatted_context)

            # Step 5: Log the query and output
            log_evaluation(query, response, [d.metadata['name'] for d in docs])

        except Exception as e:
            st.error(f"Error: {e}")


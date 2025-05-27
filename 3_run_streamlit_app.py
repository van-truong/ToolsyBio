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

# --- Sidebar settings ---
st.sidebar.header("🔧 Settings")
top_k = st.sidebar.selectbox(
    "Number of sources to retrieve (Top-K)",
    options=[1, 3, 5, 10],
    index=1  # Default to 3
)

# --- Load RAG pipeline ---
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
            # Step 1: Retrieve top-k relevant documents
            docs = retriever.get_relevant_documents(query, search_kwargs={"k": top_k})

            # Step 2: Format sources for display
            formatted_context = "\n\n".join([
                f"**{d.metadata['name']}** — [source]({d.metadata['source']})"
                for d in docs
            ])

            # Step 3: Generate LLM response
            response = chain.invoke(query)

            # Step 4: Display output
            st.subheader("💡 Answer")
            st.markdown(response)
            st.markdown("---")
            st.subheader("📚 Top Sources")
            st.markdown(formatted_context)

            # Step 5: Log interaction
            log_evaluation(query, response, [d.metadata['name'] for d in docs])

        except Exception as e:
            st.error(f"Error: {e}")
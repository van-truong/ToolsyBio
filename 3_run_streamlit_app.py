### 3_run_streamlit_app.py
"""
Streamlit front end to interact with the RAG assistant.
"""
import streamlit as st
from rag_chain import load_vector_store, setup_rag_chain
from eval_logger import log_evaluation

st.set_page_config(page_title="ToolsyBio - RAG Demo", layout="wide")
st.title("🔬 ToolsyBio: Bioinformatics Tool Advisor")
st.markdown("""
Ask any question about bioinformatics software tools indexed in `bio.tools`.
Powered by a local LLM (Ollama) and vector search using LangChain.
""")

@st.cache_resource
def get_rag():
    vs = load_vector_store()
    chain, retriever = setup_rag_chain(vs)
    return chain, retriever

chain, retriever = get_rag()

query = st.text_input("🔍 Ask a question:", placeholder="e.g. What tools do differential expression analysis?")
if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        try:
            docs = retriever.get_relevant_documents(query)
            formatted_context = "\n\n".join([f"**{d.metadata['name']}** — [source]({d.metadata['source']})" for d in docs])
            response = chain.invoke(query)
            st.subheader("💡 Answer")
            st.markdown(response)
            st.markdown("---")
            st.subheader("📚 Top Sources")
            st.markdown(formatted_context)
            # After generating response:
            log_evaluation(query, response, [d.metadata['name'] for d in docs])

        except Exception as e:
            st.error(f"Error: {e}")


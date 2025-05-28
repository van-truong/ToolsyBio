# 🔬 ToolsyBio

**ToolsyBio** is a modular, open-source system that helps researchers navigate the bioinformatics software landscape using **retrieval-augmented generation (RAG)**. It combines metadata from [bio.tools](https://bio.tools) with vector search and a local large language model (LLM) served through [Ollama](https://ollama.com/), enabling users to ask natural language questions about software tools.

📝 **Paper**:  
> (Under review) Truong, V.Q., & Ritchie, M.D. (2025). *ToolsyBio: A retrieval-augmented generation system for navigating the bioinformatics software landscape.* Proceedings of US-RSE 2025.

---

## 📁 Project Structure
```
ToolsyBio/
│
├── data/ ← Output folder for tool metadata JSON
│ └── biotools_data.json
│
├── logs/ ← Logs generated from queries
│ └── eval_results.json
│
├── 1_fetch_biotools.py ← Fetches tool data from bio.tools API
├── 2_build_vector_store.py ← Builds Chroma vector store from metadata
├── 3_run_streamlit_app.py ← Streamlit frontend for interactive queries
├── rag_chain.py ← Loads RAG chain (retriever + LLM)
├── eval_logger.py ← Saves query/response logs to JSON
├── requirements.txt ← Python dependencies
├── README.md ← You are here!
├── LICENSE ← MIT License
```

---
> 📘 Developer tips and tuning options (e.g., custom tool fetch count, resetting vector DB) are available in [DEV_GUIDE.md](./docs/DEV_GUIDE.md).


---

## Environment Setup

ToolsyBio has been tested with `Python 3.10`. Other versions (`3.9–3.11`) may also work, but 3.10 is recommended for compatibility with LangChain and ChromaDB.

Simply clone this repository, `cd` into it, and run the provided scripts. Below are some environment configurations.

### Option 1: Using Conda (recommended)

```bash
conda create -n toolsybio python=3.9 -y
conda activate toolsybio
pip install -r requirements.txt
```
### Option 2: Using venv

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Dependencies
ToolsyBio depends on the following libraries (in `requirements.txt`):

```
streamlit
tqdm
requests
langchain
sentence-transformers
chromadb
```
ToolsyBio also uses a local LLM served via Ollama. Be sure to install the version that works with your local environment.

## Step 1: Fetch tool metadata from bio.tools
This script retrieves tens of thousands of tools, formats metadata, and saves to `data/biotools_data.json`. 

In the paper, we test a subset of 5,794 tools. Under `params=`, we set the field `"q": "sequence analysis", # General keyword search`, which limits the fetch to 5,794 sequence analysis tools. If this line is edited or commented out, the fetch won't be constrained to that particular subset.

```
python 1_fetch_biotools.py
```

## Step 2: Build the vector store (RAG knowledge base)
Embeds tool descriptions using `all-MiniLM-L6-v2` and stores them in ChromaDB.

```
python 2_build_vector_store.py
```

## Step 3: Launch the browser app locally
Make sure the model you want has been pulled from Ollama and is ready before running the app. 

```
streamlit run 3_run_streamlit_app.py
```

Then visit http://localhost:8501 in your browser.


## Example Queries

You can ask questions like:
* What FOSS tools support differential gene expression analysis?
* What command-line tools support BAM format?
* What tools help with gene prediction and clustering in viral genomes?
* What tools integrate with Python or R for visualization?

Results are grounded in retrieved tool metadata and include documentation/homepage links.


## 🧾 Citation

If you use ToolsyBio in your work, please cite the GitHub repository while our paper is under review at US-RSE'25:

> Truong, V.Q, Ritchie, M.D. (2025). ToolsyBio: A Retrieval-Augmented Generation System for Navigating the Bioinformatics Software Landscape. GitHub repository: [https://github.com/van-truong/ToolsyBio](https://github.com/van-truong/ToolsyBio)

You can also use this BibTeX entry:

```bibtex
@misc{toolsybio2025,
  author       = {Van Q. Truong, Marylyn D. Ritchie},
  title        = {ToolsyBio: A retrieval-augmented generation system for navigating the bioinformatics software landscape},
  year         = {2025},
  howpublished = {\url{https://github.com/van-truong/ToolsyBio}},
  note         = {Accessed: [Insert access date here]}
}
```

## License

ToolsyBio is open-source software released under the [MIT License](./LICENSE). You are free to use, modify, and distribute it with proper attribution.

## Acknowledgments
* Tool metadata provided by the bio.tools registry
* Ontological annotations powered by the EDAM ontology
* Local model serving via Ollama


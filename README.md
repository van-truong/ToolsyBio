# 🔬 ToolsyBio

**ToolsyBio** is a modular, open-source system that helps researchers navigate the bioinformatics software landscape using **retrieval-augmented generation (RAG)**. It combines metadata from [bio.tools](https://bio.tools) with vector search and a local large language model (LLM) served through [Ollama](https://ollama.com/), enabling users to ask natural language questions about software tools.

📝 **Paper**:  
> (Under review) Truong, V.Q., & Ritchie, M.D. (2025). *ToolsyBio: A retrieval-augmented generation system for navigating the bioinformatics software landscape.* Proceedings of US-RSE 2025. [PDF](./US-RSE25_submission_112.pdf)

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
├── fetch_biotools.py ← Script to fetch tool data from bio.tools API
├── rag_pipeline.py ← Builds Chroma vector store from metadata
├── rag_chain.py ← Loads RAG chain (retriever + LLM)
├── streamlit_app.py ← Streamlit frontend for interactive queries
├── eval_logger.py ← Saves query/response logs to JSON
├── run_batch_eval.py ← (Optional) Batch evaluation script
├── requirements.txt ← Python dependencies
├── README.md ← You are here!
├── US-RSE25_submission_112.pdf ← Paper
└── CITATION.cff ← Citation metadata
```

---
> 📘 Developer tips and tuning options (e.g., custom tool fetch count, resetting vector DB) are available in [DEV_GUIDE.md](./docs/DEV_GUIDE.md).


---

## ⚙️ Setup

Install Python 3.9+ and dependencies:

```bash
pip install -r requirements.txt
```
## Requirements
```
streamlit
tqdm
requests
langchain
sentence-transformers
chromadb
```

## Step 1: Fetch tool metadata from bio.tools
This script retrieves up to 25,000 tools, formats metadata, and saves to JSON.

```
python fetch_biotools.py
```

## Step 2: Build the vector store (RAG knowledge base)
Embeds tool descriptions using all-MiniLM-L6-v2 and stores in ChromaDB.

```
python rag_pipeline.py
```

## Step 3: Launch the web app

```
streamlit run streamlit_app.py
```

Then visit http://localhost:8501 in your browser.


## Example Queries

You can ask questions like:
* What FOSS tools support differential gene expression analysis?
* What command-line tools support BAM format?
* What tools help with gene prediction and clustering in viral genomes?
* What tools integrate with Python or R for visualization?

Results are grounded in retrieved tool metadata and include documentation/homepage links.

## Batch Evaluation (Optional)
Run a predefined set of queries and log outputs:

```
python run_batch_eval.py
```




## Citation
If you use ToolsyBio in your work, please cite the US-RSE 2025 paper (see below or CITATION.cff).
```

---

### 📘 CITATION.cff

```yaml
cff-version: 1.2.0
message: "If you use ToolsyBio in your work, please cite the following paper:"
title: "ToolsyBio: A Retrieval-Augmented Generation System for Navigating the Bioinformatics Software Landscape"
authors:
  - family-names: Truong
    given-names: Van Q.
    orcid: https://orcid.org/0000-0002-5485-1818
  - family-names: Ritchie
    given-names: Marylyn D.
    orcid: https://orcid.org/0000-0002-1208-1720
date-released: 2025-05-19
abstract: >
  ToolsyBio is a modular retrieval-augmented generation (RAG) system that helps researchers explore bioinformatics software using natural language queries. Built on metadata from bio.tools and enriched with EDAM ontology terms, it uses vector-based semantic search and locally served LLMs to return grounded, trustworthy responses.
version: "v1.0"
license: "MIT"
repository-code: https://github.com/van-truong/ToolsyBio
url: https://github.com/van-truong/ToolsyBio
```

## Acknowledgments
* Tool metadata provided by the bio.tools registry
* Ontological annotations powered by the EDAM ontology
* Local model serving via Ollama


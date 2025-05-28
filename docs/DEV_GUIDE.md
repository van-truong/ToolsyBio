# 🛠️ ToolsyBio Developer Guide

This guide provides notes for contributors and power users working with ToolsyBio. It covers metadata fetch options, vector store resets, and optimization tips beyond the main [README](../README.md).

**Last updated:** May 2025  
**Applies to:** ToolsyBio v1.0 (US-RSE'25 release)

---

## 🚀 Cloning the Repository

To get started:

```bash
git clone https://github.com/van-truong/ToolsyBio.git
cd ToolsyBio
```

## 🧪 Environment Setup
ToolsyBio has been tested with `Python 3.10`. Other versions (`3.9–3.11`) may also work, but 3.10 is recommended for compatibility with LangChain and ChromaDB. You can use either Conda or venv.

### Option 1: Using Conda (recommended)
```bash
conda create -n toolsybio python=3.9 -y
conda activate toolsybio
pip install -r requirements.txt
```

### Option 2: Using venv
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment & Dependency Notes
Ensure your requirements.txt includes:
```
streamlit
tqdm
requests
langchain
sentence-transformers
chromadb
```

And that Ollama is installed and running. For some user, you will start the Ollama service via the desktop application, while others can start it within a terminal window and leave it running in a separate terminal while using ToolsyBio.

You can use any Ollama models. For the purpose of the paper, we tested ToolsyBio with `mistral:7b`. 

```
ollama serve
```

```
ollama pull mistral:7b # Pulls the model from https://ollama.com/library/mistral
```

## ⚙️ Fetching Tools from bio.tools
ToolsyBio can fetch either all tools or a filtered subset from the bio.tools API.

You can switch the default so ToolsyBio fetches **all tools available in the bio.tools registry** (over 30,000 tools).

You can also filter this for a smaller or domain-specific subset by modifying the query parameters in `1_fetch_biotools.py`.

### To Fetch All Tools (Full Registry)
In `1_fetch_biotools.py`, make sure the query filter (`"q"`) is removed or commented out:

```python
params = {
    "format": "json",
    "page": 1,
    "sort": "last_update",
    "ord": "desc"
}
```

To test with a smaller subset, open `1_fetch_biotools.py` and change:

```python
MAX_TOOLS_TO_FETCH = 100  # Small test set
```

To fetch the entire catalog (recommended for production):

```python
MAX_TOOLS_TO_FETCH = 40000
```

### To Fetch a Subset (e.g., for Testing or Domain-Specific Use)
This filtered configuration was used in the original US-RSE’25 submission, resulting in a test set of approximately 5,794 tools.

You can also change these params to include a different keyword or EDAM topic filter:

```python
params = {
    "format": "json",
    "page": 1,
    "q": "sequence analysis",  # Only tools matching this query
    "sort": "last_update",
    "ord": "desc"
}
```

## Performance Tip: Rate Limiting
The script includes polite waits to avoid API rate limits. You can speed it up slightly by adjusting the delay in 1_fetch_biotools.py:

```python
time.sleep(0.2)  # Between individual tool detail requests
```
Warning: Do not reduce this below 0.1 seconds or you risk getting blocked by the API.

## Resetting the Vector Store (Optional)
Chroma overwrites contents when you rebuild, but a manual reset is useful when:
* You change the chunking strategy
* You switch to a new embedding model
* Retrieval starts returning stale or incorrect results
* You want a full clean rebuild

To delete:

```bash
rm -rf chroma_db/
```

## Rebuilding the Vector Store (ChromaDB)
The RAG system splits each tool’s metadata into text chunks, embeds them, and stores them in ChromaDB.

Run:

```bash
python 2_build_vector_store.py
```

This script:
* Loads and flattens metadata from `data/biotools_data.json`
* Splits each tool into overlapping ~1000-character chunks
* Embeds using `all-MiniLM-L6-v2`
* Saves the result to `chroma_db/`

✅ Sample output:
```
📦 Vector store created at: chroma_db
✅ Vector database build complete.
```

## Sample Output Preview (Fetch)
Below is an example of what the fetcher logs when retrieving tools:

```
Fetching details for: polydot_ws_husar
Fetching details for: supermatcher_ws_husar
...
Fetched 5794 tools in total.
Data saved to biotools_data.json
```

## Sample tool record:
```
--- Tool 1 (openms) ---
Tool Name: OpenMS
Description: Open source library for mass spectrometry data analysis...
Functions: Protein identification, Peak detection, ...
Topics: Proteomics, Metabolomics
Homepage: http://www.openms.de
Documentation: http://ftp.mi.fu-berlin.de/...
```

## Example Prompts for Testing
These queries were used in the paper:
* "What FOSS tools support differential gene expression analysis?"
* "What command-line tools support BAM format?"
* "What tools help with gene prediction and clustering in viral genomes?"
* "What tools integrate with Python or R for visualization?"

## Questions?
For help extending the tool, adding new sources, or updating the embedding method, feel free to open a GitHub issue or pull request (PR).
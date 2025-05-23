# 🛠️ ToolsyBio Developer Guide

This document includes advanced notes for power users and contributors working with ToolsyBio. It covers metadata fetch options, vector store reset instructions, and debug tips that go beyond the main [README](../README.md).

---

## ⚙️ Fetching More Tools from bio.tools

By default, ToolsyBio is configured to retrieve **all tools available in bio.tools** (up to 25,000+ tools).

To reduce scope (e.g. for testing), open `fetch_biotools.py` and edit:

```python
MAX_TOOLS_TO_FETCH = 100  # For a small demo
```

To fetch the entire catalog (recommended for production):

```python
MAX_TOOLS_TO_FETCH = 25000
```

## Performance Tip: Rate Limiting
The script includes polite waits to avoid API rate limits. You can speed it up slightly by adjusting the delay in fetch_biotools.py:

```python
time.sleep(0.2)  # Between individual tool detail requests
```
Warning: Do not reduce this below 0.1 seconds or you risk getting blocked by the API.

## Resetting the Vector Store (Optional)
You usually do not need to manually delete the vector store, as Chroma.from_documents() will overwrite the contents of the existing directory.
However, delete the store if:
* You change the chunking strategy
* You switch to a new embedding model
* Retrieval starts returning stale or incorrect results
* You want a full clean rebuild

To delete:

```bash
rm -rf chroma_db/
```

## Rebuilding the Vector Database
The RAG system splits each tool into text chunks, embeds them, and stores them in ChromaDB.

Run:

```bash
python rag_pipeline.py
```

What it does:
* Loads and flattens metadata from data/biotools_data.json
* Splits each tool into overlapping ~1000-character chunks
* Embeds using all-MiniLM-L6-v2

Saves the result to chroma_db/

✅ Output:
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

## Sample tool entry:
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

## Running Batch Evaluation (for consistency testing)
Use the batch evaluation script to test queries from the paper:

```
python run_batch_eval.py
```

Each query will:
* Trigger RAG retrieval and LLM response
* Save results to logs/eval_results.json

You can review the JSON logs to validate tool matches and evaluate grounding fidelity.


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

And that Ollama is installed and running:
```
ollama serve
ollama pull mistral
```

## Questions?
For help extending the tool, adding new sources, or updating the embedding method, feel free to open a GitHub issue or pull request (PR).
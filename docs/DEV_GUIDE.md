# 🛠️ ToolsyBio Developer Guide

This guide provides notes for contributors and power users working with ToolsyBio. It covers metadata fetch options, vector store resets, and optimization tips beyond the main [README](../README.md).

**Last updated:** May 2025  
**Applies to:** ToolsyBio v1.0 (US-RSE'25 release)

---

## ⚙️ Fetching Tools from bio.tools

ToolsyBio can retrieve up to **25,000+ tools** from the [bio.tools](https://bio.tools) API.

To test with a smaller subset, open `1_fetch_biotools.py` and change:

```python
MAX_TOOLS_TO_FETCH = 100  # Small test set
```

To fetch the entire catalog (recommended for production):

```python
MAX_TOOLS_TO_FETCH = 25000
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
The RAG system splits each tool into text chunks, embeds them, and stores them in ChromaDB.

Run:

```bash
python 2_build_vector_store.py
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
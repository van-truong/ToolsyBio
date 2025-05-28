# eval_logger.py
# --------------------------------------------
# Logs each query-answer interaction as a separate JSON file.
# Filename includes timestamp and retrieval parameter (top-k).
# --------------------------------------------

import json
import os
from datetime import datetime

LOG_DIR = "logs/queries"

def log_evaluation(query, answer, sources):
    """
    Saves a query-answer interaction to a timestamped JSON file.

    Parameters:
        query (str): The user's input question
        answer (str): The model's generated response
        sources (list of str): List of retrieved tool names or sources
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    # Format filename: query_20240527_113215_k3.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{LOG_DIR}/query_{timestamp}.json"

    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "sources": sources
    }

    with open(filename, "w") as f:
        json.dump(record, f, indent=2)

    print(f"✅ Saved log to {filename}")

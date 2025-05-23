import json
import os
from datetime import datetime

LOG_PATH = "logs/eval_results.json"

def log_evaluation(query, answer, sources):
    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "sources": sources
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Logged query to {LOG_PATH}")

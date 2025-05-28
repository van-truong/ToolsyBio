# 1_fetch_biotools.py
# --------------------------------------------
# This script fetches tool metadata from the bio.tools API.
# It can retrieve either all tools (≈30,000+) or a filtered subset
# (e.g., "sequence analysis" tools as used in the US-RSE'25 paper).
#
# It supports resume mode by skipping already-fetched tool IDs and
# saving after each page to avoid data loss.
# Output: data/biotools_data.json
# --------------------------------------------

import requests
import json
import time
import os

# --- API Configuration ---
BIOTOOLS_API_URL = "https://bio.tools/api/t"

params = {
    "format": "json",
    "page": 1,
    "q": "sequence analysis",  # Comment this out to fetch ALL tools
    "sort": "last_update",
    "ord": "desc"
}

# --- Constants ---
MAX_TOOLS_TO_FETCH = 40000
OUTPUT_FILENAME = "data/biotools_data.json"

def load_existing_tools():
    """
    Loads previously saved tools (if any) and returns:
    - list of tool dicts
    - set of tool IDs already fetched
    """
    os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

    if os.path.exists(OUTPUT_FILENAME):
        with open(OUTPUT_FILENAME, "r") as f:
            data = json.load(f)
        ids = {t["id"] for t in data if "id" in t}
        print(f"🔄 Resume mode: {len(ids)} tools already saved.")
        return data, ids
    return [], set()

def fetch_tools_data(max_tools=MAX_TOOLS_TO_FETCH):
    """Fetches tool metadata page-by-page, skipping already saved entries."""
    tools_data, seen_ids = load_existing_tools()
    page = 1
    fetched_count = len(seen_ids)

    while fetched_count < max_tools:
        current_params = params.copy()
        current_params["page"] = page
        print(f"📄 Fetching page {page} with params: {current_params}")

        try:
            response = requests.get(BIOTOOLS_API_URL, params=current_params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if not data.get('list'):
                print("No more tools found or empty list.")
                break

            new_this_page = 0

            for tool in data['list']:
                if fetched_count >= max_tools:
                    break

                tool_id = tool.get('biotoolsID')
                if not tool_id:
                    print(f"⚠️ Skipping tool without biotoolsID: {tool.get('name')}")
                    continue
                if tool_id in seen_ids:
                    continue  # Skip already fetched tools

                try:
                    print(f"🔍 Fetching details for: {tool_id}")
                    detail_url = f"https://bio.tools/api/t/{tool_id}?format=json"
                    detail_response = requests.get(detail_url, timeout=30)
                    detail_response.raise_for_status()
                    tool_details = detail_response.json()

                    name = tool_details.get('name', 'N/A')
                    description = tool_details.get('description', 'N/A')

                    functions = []
                    if tool_details.get('function'):
                        for func in tool_details['function']:
                            operations = [op.get('term', 'N/A') for op in func.get('operation', []) if op.get('term')]
                            functions.extend(operations)
                    functions_str = ", ".join(sorted(set(functions))) if functions else "N/A"

                    topics = [topic.get('term', 'N/A') for topic in tool_details.get('topic', []) if topic.get('term')]
                    topics_str = ", ".join(sorted(set(topics))) if topics else "N/A"

                    homepage = tool_details.get('homepage', 'N/A')
                    docs_url = ""
                    if tool_details.get('documentation'):
                        docs_url = tool_details['documentation'][0].get('url', 'N/A')

                    combined_text = (
                        f"Tool Name: {name}\n"
                        f"Description: {description}\n"
                        f"Functions: {functions_str}\n"
                        f"Topics: {topics_str}\n"
                        f"Homepage: {homepage}\n"
                        f"Documentation: {docs_url}\n"
                    )

                    tools_data.append({
                        "id": tool_id,
                        "name": name,
                        "text_content": combined_text,
                        "source": detail_url
                    })

                    seen_ids.add(tool_id)
                    fetched_count += 1
                    new_this_page += 1
                    time.sleep(0.2)  # Be respectful to the API

                except requests.exceptions.RequestException as e_detail:
                    print(f"❌ Error fetching details for {tool_id}: {e_detail}")
                except json.JSONDecodeError as e_json_detail:
                    print(f"❌ Error decoding JSON for {tool_id}: {e_json_detail}")

            # ✅ Save after each page
            with open(OUTPUT_FILENAME, 'w') as f:
                json.dump(tools_data, f, indent=4)
            print(f"💾 Saved {fetched_count} tools total. (+{new_this_page} new on this page)")

            if not data.get('next'):
                print("✅ No more pages.")
                break

            page += 1
            if fetched_count >= max_tools:
                print(f"✅ Reached max tools: {fetched_count}")
                break

            time.sleep(0.5)  # Delay between page requests

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching page {page}: {e}")
            break
        except json.JSONDecodeError:
            print(f"❌ Error decoding JSON on page {page}.")
            break

    return tools_data

# --- Entry Point ---
if __name__ == "__main__":
    print("🚀 Starting tool fetch from bio.tools...")
    all_tools = fetch_tools_data()
    print(f"✅ Finished. Fetched {len(all_tools)} tools.")

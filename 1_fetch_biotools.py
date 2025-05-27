# 1_fetch_biotools.py
# --------------------------------------------
# This script fetches tool metadata from the bio.tools API.
# It can retrieve either all tools (≈30,000+) or a filtered subset
# (e.g., "sequence analysis" tools as used in the US-RSE'25 paper).
#
# Output: A JSON file of structured tool entries used as input for RAG.
# --------------------------------------------

import requests
import json
import time


# --- API Configuration ---
# The query parameter "q" filters tools by keyword.
# Example used in the paper: q = "sequence analysis" (~5,794 tools).
# To fetch the full registry, REMOVE the "q" line below.
BIOTOOLS_API_URL = "https://bio.tools/api/t"

params = {
    "format": "json",
    "page": 1,
    "q": "sequence analysis", # Comment out to fetch ALL tools
    "sort": "last_update", # Sort by last update to get more recent tools potentially
    "ord": "desc"
}

# --- Constants ---
# Maximum number of tools to fetch.
MAX_TOOLS_TO_FETCH = 40000 # 200 to grab proof of concept, 40000 to safely capture the full dataset

def fetch_tools_data(max_tools=MAX_TOOLS_TO_FETCH):
    """Fetches tool metadata from the bio.tools API."""
    tools_data = []
    page = 1
    fetched_count = 0

    while fetched_count < max_tools:
        current_params = params.copy()
        current_params["page"] = page
        print(f"Fetching page {page} with params: {current_params}")

        try:
            response = requests.get(BIOTOOLS_API_URL, params=current_params, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            if not data.get('list'):
                print("No more tools found or empty list.")
                break

            for tool in data['list']:
                if fetched_count >= max_tools:
                    break
                try:
                    # Fetch full details for each tool
                    tool_id = tool.get('biotoolsID')
                    if not tool_id:
                        print(f"Skipping tool without biotoolsID: {tool.get('name')}")
                        continue

                    print(f"Fetching details for: {tool_id}")
                    detail_url = f"https://bio.tools/api/t/{tool_id}?format=json"
                    detail_response = requests.get(detail_url, timeout=30)
                    detail_response.raise_for_status()
                    tool_details = detail_response.json()

                    # Extract relevant fields from the detailed record
                    name = tool_details.get('name', 'N/A')
                    description = tool_details.get('description', 'N/A')

                    functions = []
                    if tool_details.get('function'):
                        for func in tool_details['function']:
                            operations = [op.get('term', 'N/A') for op in func.get('operation', []) if op.get('term')]
                            functions.extend(operations)
                    functions_str = ", ".join(list(set(functions))) if functions else "N/A"

                    topics = [topic.get('term', 'N/A') for topic in tool_details.get('topic', []) if topic.get('term')]
                    topics_str = ", ".join(list(set(topics))) if topics else "N/A"

                    homepage = tool_details.get('homepage', 'N/A')
                    docs_url = ""
                    if tool_details.get('documentation'):
                       docs_url = tool_details['documentation'][0].get('url', 'N/A')


                    # Combine into a single text block for easier processing later for RAG
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
                    fetched_count += 1
                    time.sleep(0.2) # Respectful delay for individual requests

                except requests.exceptions.RequestException as e_detail:
                    print(f"Error fetching details for {tool.get('biotoolsID', 'Unknown tool')}: {e_detail}")
                except json.JSONDecodeError as e_json_detail:
                    print(f"Error decoding JSON for {tool.get('biotoolsID', 'Unknown tool')}: {e_json_detail}")


            if not data.get('next'):
                print("No more pages.")
                break
            page += 1
            if fetched_count >= max_tools:
                print(f"Reached max tools to fetch: {fetched_count}")
                break
            time.sleep(0.5) # Polite delay between page fetches

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        except json.JSONDecodeError:
            print(f"Error decoding JSON from page {page}. Content: {response.text[:200]}")
            break

    return tools_data

# --- Entry Point ---
if __name__ == "__main__":
    print("Fetching bio.tools data...")
    all_tools = fetch_tools_data()
    print(f"\nFetched {len(all_tools)} tools in total.")

    # Save to a JSON file
    output_filename = "biotools_data.json"
    with open(output_filename, 'w') as f:
        json.dump(all_tools, f, indent=4)
    print(f"Data saved to {output_filename}")

    # Example: Print info for the first few tools
    for i, tool_doc in enumerate(all_tools[:3]):
        print(f"\n--- Tool {i+1} ({tool_doc['id']}) ---")
        print(tool_doc['text_content'])
from dotenv import load_dotenv
import os
import requests
import json

def determine_task(task_description: str):
    """
    Given a task description (which may be phrased in various ways),
    call the LLM to map it to one of the canonical tasks and, if the task is A1,
    extract the relevant script URL from the description.
    
    The LLM is expected to return its answer as a Markdown-formatted JSON code block,
    for example:
    
    ```json
    {
      "task": "A1",
      "url": "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    }
    ```
    
    This function removes any Markdown formatting and returns a tuple: (task_id, url),
    where the url is non-empty only for task A1.
    """
    load_dotenv()
    api_token = os.getenv("OPENAI_API_KEY", "localhost:5432")
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    
    if not api_token or api_token == "localhost:5432":
        raise RuntimeError("API token not found in environment variables")
    
    prompt_system = (
        "You are an assistant that receives a task description and maps it to one of the following canonical tasks:\n\n"
        "A1: Install uv (if required) and run the datagen script from URL https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py with the user's email as its only argument.\n\n"
        "A2: Format the contents of /data/format.md using prettier@3.4.2, updating the file in-place.\n\n"
        "A3: Count the number of a specific weekday in a file (for example, /data/dates.txt) and write the count to an output file.\n\n"
        "A4: Sort the array of contacts in /data/contacts.json by last_name, then first_name, and write the result to /data/contacts-sorted.json.\n\n"
        "A5: Write the first line of the 10 most recent .log files in /data/logs/ to /data/logs-recent.txt.\n\n"
        "A6: Find all Markdown (.md) files in /data/docs/, extract the first occurrence of an H1 line (starting with '# '), and create an index file /data/docs/index.json mapping each filename (relative to /data/docs/) to its title.\n\n"
        "A7: Extract the sender’s email address from /data/email.txt and write it to /data/email-sender.txt.\n\n"
        "A8: Extract the credit card number from /data/credit-card.png using an LLM and write it (with no spaces) to /data/credit-card.txt.\n\n"
        "A9: Using embeddings, find the most similar pair of comments from a file (e.g., /data/comments.txt) and write them (one per line) to an output file.\n\n"
        "A10: Compute the total sales for all bids of 'Gold' tickets from the SQLite database /data/ticket-sales.db (table 'tickets' with columns type, units, and price) and write the number to /data/ticket-sales-gold.txt.\n\n"
        "Your job is to return the canonical task identifier that best matches the input description. If the description corresponds to task A1, also extract the script URL from the description. "
        "Return your answer as JSON with keys 'task' and 'url'."
    )
    
    prompt_user = f"Task description: {task_description}\nExtracted information:"
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    
    if "choices" in response_data and len(response_data["choices"]) > 0:
        raw_content = response_data["choices"][0]["message"]["content"].strip()
        # Remove markdown code block formatting if present
        if raw_content.startswith("```json"):
            raw_content = raw_content[len("```json"):].strip()
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3].strip()
        try:
            extracted_info = json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON from LLM response: {e}\nResponse content: {raw_content}")
        
        task_id = extracted_info.get("task")
        url = extracted_info.get("url", "") if task_id == "A1" else ""
        return task_id, url
    else:
        raise RuntimeError("Failed to determine task identifier and URL from LLM response")

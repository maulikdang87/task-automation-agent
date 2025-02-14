import json
import os
import re

def A6():
    """
    Find all .md files in /data/docs/, extract the first occurrence of an H1 title (# Title),
    and save them in /data/docs/index.json as { "file.md": "Title", ... }.
    """
    docs_dir = os.path.join(os.getcwd(), "data", "docs")
    output_file = os.path.join(docs_dir, "index.json")

    index = {}

    # Walk through /data/docs/ recursively
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, docs_dir)

                # Extract the first H1 title from the file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            match = re.match(r"^# (.+)", line.strip())
                            if match:
                                index[relative_path] = match.group(1)
                                break  # Stop after first H1
                except Exception as e:
                    index[relative_path] = f"Error reading file: {str(e)}"

    # Write to index.json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    return {"written_file": output_file, "index": index}
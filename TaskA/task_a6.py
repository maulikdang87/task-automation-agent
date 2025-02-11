import os
import json

def index_markdown_files():
    docs_dir = "./data/docs"
    index_file = "./data/docs/index.json"
    index = {}

    if not os.path.isdir(docs_dir):
        raise FileNotFoundError("Docs directory not found")

    try:
        for root, _, files in os.walk(docs_dir):  # Recursively walk through subdirectories
            for file in files:
                if file.endswith(".md"):
                    relative_path = os.path.relpath(os.path.join(root, file), docs_dir)  # Get relative path
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("# "):
                                index[relative_path] = line[2:].strip()  # Store without prefix
                                break  # Only take the first H1

        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)

        return "Markdown files indexed successfully."
    except Exception as e:
        raise RuntimeError(f"Error indexing markdown files: {e}")

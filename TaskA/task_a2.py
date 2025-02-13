import os
import subprocess

def is_npx_installed():
    try:
        result = subprocess.run(
            ["npx", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("npx version:", result.stdout.strip())
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def format_markdown():
    file_path = "data/format.md"
    if not os.path.isfile(file_path):
        raise RuntimeError(f"File '{file_path}' not found.")
    
    if not is_npx_installed():
        raise RuntimeError("npx is not installed. Please install npm (npx is bundled with npm).")
    
    try:
        result = subprocess.run(
            ["npx", "prettier@3.4.2", "--parser", "markdown", "--stdin-filepath", file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("npx prettier output:", result.stdout)
        return "Markdown formatting completed successfully."
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to format markdown: {e.stderr}")


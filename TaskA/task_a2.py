import subprocess


def is_npm_installed():
    try:
        subprocess.run(["npm", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def is_prettier_installed():
    try:
        subprocess.run(["prettier", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_prettier():
    if not is_npm_installed():
        raise RuntimeError("npm is not installed. Please install npm first.")
    try:
        subprocess.run(["npm", "install", "-g", "prettier@3.4.2"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install Prettier: {e}")

def format_markdown():
    file_path = "./data/format.md"
    if not is_prettier_installed():
        install_prettier()
    try:
        subprocess.run(["prettier", "--write", file_path], check=True)
        return "Markdown formatting completed successfully."
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to format markdown: {e}")

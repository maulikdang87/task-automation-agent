from fastapi import FastAPI, Query, HTTPException

import os
import subprocess
import requests

app = FastAPI()

def is_uv_installed():
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_uv():
    if not is_uv_installed():
        try:
            subprocess.run(["pip", "install", "uv"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install uv: {e}")

def download_and_patch_datagen():
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    file_path = "datagen.py"
    output_dir = "./data"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        script_content = response.text.replace("/data", output_dir)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(script_content)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to download and patch datagen.py: {e}")

def run_datagen(user_email: str):
    try:
        install_uv()
        file_path = download_and_patch_datagen()
        subprocess.run(["uv","run", file_path, user_email], check=True)
        return "Data generation completed successfully."
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to execute datagen.py: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
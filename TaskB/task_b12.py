# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import requests

def B12(filepath):
    if filepath.startswith('/data'):
        response = requests.get(f"http://localhost:8000/read?path={filepath}")
        with open("response.txt", "w") as f:
            f.write(response.text)
        
        return response.text
    else:
        return False

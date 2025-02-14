import re
import requests
import shutil 
import subprocess
import os
def A1(user_email: str ,script_url : str):
    # 1. Check if 'uv' is installed.
    if shutil.which("uv") is None:
        try:
            install_proc = subprocess.run(
                ["pip", "install", "uv"],
                check=True,
                capture_output=True,
                text=True
            )
            print("Installed uv:", install_proc.stdout)
        except subprocess.CalledProcessError as e:
            raise Exception("Failed to install uv: " + e.stderr)
    
    # 2. Download the datagen.py script.
    datagen_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    response = requests.get(datagen_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download datagen.py, status code: {response.status_code}")
    
    datagen_filename = "datagen.py"
    with open(datagen_filename, "w") as f:
        f.write(response.text)
    
    # 3. Modify the script to use a local data folder instead of '/data'.
    #    We'll assume your local folder is the 'data' directory in your project.
    local_data_dir = os.path.join(os.getcwd(), "data")
    
    # Read the downloaded file
    with open(datagen_filename, "r") as f:
        content = f.read()
    
    # Replace occurrences of '/data' (in quotes) with the local data directory.
    # This regex will match both single and double quotes.
    new_content = re.sub(r'([\'"])/data([\'"])', f'\\1{local_data_dir}\\2', content)
    
    # Write the modified content back to datagen.py
    with open(datagen_filename, "w") as f:
        f.write(new_content)
    
    # 4. Run datagen.py with the user's email as the only argument.
    try:
        proc = subprocess.run(
            ["python", datagen_filename, user_email],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise Exception("Error running datagen.py: " + e.stderr)
    
    return {"stdout": proc.stdout, "stderr": proc.stderr}

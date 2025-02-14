import os
import subprocess

def A2():
    """
    Formats the file /data/format.md using prettier@3.4.2.
    The file is updated in-place.
    
    This version mimics the evaluation script: it pipes the file content into Prettier
    using the "--stdin-filepath /data/format.md" option.
    """
    # Define the local data directory (project-root/data)
    local_data_dir = os.path.join(os.getcwd(), "data")
    
    # Construct the local file path for format.md
    file_path = os.path.join(local_data_dir, "format.md")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    
    # Read the current contents of the file.
    with open(file_path, "r") as f:
        original = f.read()
        
    import os
    
    try:
        # Build the command as a single string.
        cmd = "npx prettier@3.4.2 --stdin-filepath /data/format.md"
        # Run Prettier using the command string, passing the current working directory and environment.
        proc = subprocess.run(
            cmd,
            input=original,
            capture_output=True,
            text=True,
            check=True,
            # shell=True,  # Command is provided as a string.
            cwd=os.getcwd(),         # Ensure we run in the project root.
            env=os.environ.copy()      # Pass the current environment.
        )
        formatted = proc.stdout
        
        # Write the formatted content back to the file.
        with open(file_path, "w") as f:
            f.write(formatted)
        
        return {"stdout": formatted, "stderr": proc.stderr}
    except subprocess.CalledProcessError as e:
        raise Exception("Error formatting file: " + e.stderr)
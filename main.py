# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi",
#     "uvicorn",
# ]
# ///
from fastapi.responses import PlainTextResponse
from TaskA.task_a1 import handle_task_A1
from TaskA.task_a2 import format_markdown
from TaskA.task_a3 import handle_task_A3
from TaskA.task_a4 import handle_task_A4
from TaskA.task_a5 import get_most_recent_logs
from TaskA.task_a6 import handle_task_A6
from TaskA.task_a7 import extract_email_sender
from TaskA.task_a8 import handle_task_A8
from TaskA.task_a9 import find_similar_comments
from TaskA.task_a10 import compute_gold_ticket_sales
from fastapi import FastAPI, Query, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from aTaskassigner import determine_task

app = FastAPI()

app = FastAPI()

# Assume determine_task and all the task functions (run_datagen, format_markdown, etc.)
# are defined as in the previous code.

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English")):
    load_dotenv()
    user_email = os.getenv("user_email")
    try:
        # Determine the canonical task and (if applicable) extract the URL.
        determined_task, script_url = determine_task(task)
        print("Determined Task:", determined_task, "Script URL:", script_url)
        
        if determined_task == "A1":
            # For A1, a user_email is required and the script URL must be provided.
            if not user_email:
                raise ValueError("Missing required parameter: user_email for task A1")
            result = handle_task_A1(user_email)
        elif determined_task == "A2":
            result = format_markdown()
            print(result)
        elif determined_task == "A3":
            result = handle_task_A3()
        elif determined_task == "A4":
            result = handle_task_A4()
        elif determined_task == "A5":
            result = get_most_recent_logs()
        elif determined_task == "A6":
            result = handle_task_A6()
        elif determined_task == "A7":
            result = extract_email_sender()
        elif determined_task == "A8":
            result = handle_task_A8()
        elif determined_task == "A9":
            result = find_similar_comments()
        elif determined_task == "A10":
            result = compute_gold_ticket_sales()
        else:
            # If LLM returned UNKNOWN or an unsupported task code.
            raise Exception("Unrecognized or unsupported task code returned by LLM.")
        
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(...)):
    """
    GET endpoint to read and return the content of a file.
    Ensures only files under /data (as specified in the task) are accessed.
    """
    # Security check: Path must start with /data
    if not path.startswith("/data"):
        raise HTTPException(status_code=400, detail="Invalid file path: Must start with /data")
    
    # Translate the given path into a local path.
    # Assuming your repository has a 'data' folder in its root,
    # we remove the leading '/data' and join with the repository's data directory.
    base_dir = os.path.join(os.getcwd(), "data")  # local data folder
    relative_path = os.path.relpath(path, "/data")  # e.g. "sample.txt"
    file_path = os.path.join(base_dir, relative_path)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

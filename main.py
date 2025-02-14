# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi",
#     "uvicorn",
# ]
# ///
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Query, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from aTaskassigner import determine_task
from fastapi.middleware.cors import CORSMiddleware
from TaskA.task_a1 import A1
from TaskA.task_a2 import A2
from TaskA.task_a3 import A3
from TaskA.task_a4 import A4
from TaskA.task_a5 import A5
from TaskA.task_a6 import A6
from TaskA.task_a7 import A7
from TaskA.task_a8 import A8
from TaskA.task_a9 import A9
from TaskA.task_a10 import A10


app = FastAPI()

# Assume determine_task and all the task functions (run_datagen, handle_task_A2, etc.)
# are defined as in the previous code.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English")):
    load_dotenv()
    user_email = "23f2001975@ds.study.iitm.ac.in"
    try:
        # Determine the canonical task and (if applicable) extract the URL.
        determined_task, script_url = determine_task(task)
        print("Determined Task:", determined_task, "Script URL:", script_url)
        
        if determined_task == "A1":
            # For A1, a user_email is required and the script URL must be provided.
            if not user_email:
                raise ValueError("Missing required parameter: user_email for task A1")
            result = A1(user_email,script_url)
        elif determined_task == "A2":
            result = A2() 
        elif determined_task == "A3":
            result = A3()
        elif determined_task == "A4":
            result = A4()
        elif determined_task == "A5":
            result = A5()
        elif determined_task == "A6":
            result = A6()
        elif determined_task == "A7":
            result = A7()
        elif determined_task == "A8":
            result = A8()
        elif determined_task == "A9":
            result = A9()
        elif determined_task == "A10":
            result = A10()
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
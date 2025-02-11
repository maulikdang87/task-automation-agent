# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi",
#     "uvicorn",
# ]
# ///

from task_a1 import run_datagen
from task_a2 import format_markdown
from task_a3 import count_wednesdays
from task_a4 import sort_contacts
from task_a5 import get_most_recent_logs
from fastapi import FastAPI, Query, HTTPException
import uvicorn
import os


app = FastAPI()

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English"), user_email: str = Query(None)):
    try:
        if "generate data" in task.lower():
            if not user_email:
                raise ValueError("Missing required parameter: user_email")
            result = run_datagen(user_email)
        elif "format markdown" in task.lower():
            result = format_markdown()
        elif "count wednesdays" in task.lower():
            result = count_wednesdays()
        elif "sort contacts" in task.lower():
            result = sort_contacts()
        else:
            raise ValueError("Task not recognized.")
        return {"status": "success", "output": result}, 200
    except ValueError as e:
        return {"status": "error", "detail": str(e)}, 400
    except Exception as e:
        return {"status": "error", "detail": f"Agent error: {str(e)}"}, 500


@app.get("/read")
async def read_file(path: str = Query(..., description="Path to the file")):
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

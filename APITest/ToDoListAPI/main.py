from fastapi import FastAPI, HTTPException  #for error handling
from pydantic import BaseModel #data validation
from typing import Optional #optional type hinting

app = FastAPI()

tasks = [] #temp database

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

@app.get("/")
def root():
    return {"message": "Hello API!"}

@app.post("/tasks/")
def create_task(task: Task):
    # Convert Pydantic model to dict and add an ID
    task = task.model_dump()
    task["id"] = len(tasks) + 1
    tasks.append(task)
    return {"message": "Task added successfully", "task": task}

@app.get("/tasks/")
def get_tasks():
    return {"tasks": tasks}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for t in tasks:
        if t["id"] == task_id:
            updated_task = task.model_dump()
            updated_task["id"] = task_id
            t.update(updated_task)
            return {"message": "Task updated successfully", "task": t}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    for t in tasks:
        if t["id"] == task_id:
            tasks = [task for task in tasks if task["id"] != task_id]
            return {"message": "Task deleted successfully"}
        
    raise HTTPException(status_code=404, detail="Task not found")
    

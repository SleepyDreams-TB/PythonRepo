from fastapi import FastAPI, HTTPException  #for error handling
from typing import Optional #optional type hinting
from fastapi import FastAPI, Form

app = FastAPI()

tasks = [] #temp database

@app.get("/")
def root():
    return {"message": "Welcome to the Task App API!"}

@app.post("/tasks/")
def create_task(
    title: str = Form(..., min_length=3, max_length=50),
    description: Optional[str] = Form(None, max_length=200),
    completed: Optional[bool] = Form(False),
    due_date: Optional[str] = Form(None),
    priority: Optional[int] = Form(1, ge=1, le=5)
):
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": completed,
        "due_date": due_date,
        "priority": priority
    }
    tasks.append(task)
    return {"message": "Task added successfully", "task": task}

@app.get("/tasks/")
def get_tasks():
    return {"tasks": tasks}

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: Optional[str] = Form(None, min_length=3, max_length=50),
    description: Optional[str] = Form(None, max_length=200),
    completed: Optional[bool] = Form(None),
    due_date: Optional[str] = Form(None),
    priority: Optional[int] = Form(None, ge=1, le=5)
):
    # Find the task
    for t in tasks:
        if t["id"] == task_id:
            # Update only provided fields
            if title is not None:
                t["title"] = title
            if description is not None:
                t["description"] = description
            if completed is not None:
                t["completed"] = completed
            if due_date is not None:
                t["due_date"] = due_date
            if priority is not None:
                t["priority"] = priority
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
    

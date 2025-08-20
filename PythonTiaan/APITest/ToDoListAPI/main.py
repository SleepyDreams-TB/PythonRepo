from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Depends, Form, status, Query #Form for form data, status for HTTP status codes, Query for query parameters
from typing import Optional #optional type hinting

# Import necessary modules for FastAPI and JWT authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # OAuth2 for token-based authentication 
from datetime import datetime, timedelta, timezone # datetime for handling dates and times
from jose import JWTError, jwt # jose for creating and verifying JWT tokens

app = FastAPI()

# --- Auth Setup ---
SECRET_KEY = "super_secret_key"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Test Database ---
test_users_db = {
    "Tiaan": {"username": "Tiaan", "password": "test123"}  # plain text for demo
}

#---Create JWT Token ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Get current user ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )

# --- Login Endpoint ---
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = test_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Task Management ---
tasks = [] #temp database

@app.get("/")
def root():
    return {"message": "Welcome to the Task App API!"}

@app.post("/tasks/")
def create_task(
    title: str = Form(..., min_length=3, max_length=50, description="Title of the task"),
    description: Optional[str] = Form(None, max_length=200, description="Optional description"),
    completed: Optional[bool] = Form(False, description="Task completion status"),
    due_date: Optional[str] = Form(None, description="Due date in YYYY-MM-DD format"),
    priority: Optional[int] = Form(1, ge=1, le=5, description="Task priority, 1=low, 5=high"),
    current_user: str = Depends(get_current_user)
):
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": completed,
        "due_date": due_date,
        "priority": priority,
        "owner": current_user
    }
    tasks.append(task)
    return {"message": "Task added successfully", "task": task}

@app.get("/tasks/")
def list_tasks(priority: Optional[int] = Query(None, description="Filter by priority"),  completed: Optional[bool] = Query(None, description="Filter by completion status"),
    current_user: str = Depends(get_current_user)):
    user_tasks = [t for t in tasks if t["owner"] == current_user]
    if priority:
        user_tasks = [t for t in user_tasks if t["priority"] == priority]
    if completed is not None:
        user_tasks = [t for t in user_tasks if t["completed"] == completed]
    return {"tasks": user_tasks}

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: Optional[str] = Form(None, min_length=3, max_length=50),
    description: Optional[str] = Form(None, max_length=200),
    completed: Optional[bool] = Form(None),
    due_date: Optional[str] = Form(None),
    priority: Optional[int] = Form(None, ge=1, le=5),
    current_user: str = Depends(get_current_user)
):
    # Find the task
    for t in tasks:
        if t["id"] == task_id and t["owner"] == current_user:
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
def delete_task(task_id: int, current_user: str = Depends(get_current_user)):
    global tasks
    for t in tasks:
        if t["id"] == task_id and t["owner"] == current_user:
            tasks = [task for task in tasks if task["id"] != task_id]
            return {"message": "Task deleted successfully"}      
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/{task_id}")
def get_task(task_id: int, current_user: str = Depends(get_current_user)):
    for t in tasks:
        if t["id"] == task_id and t["owner"] == current_user:
            return {"task": t}
    raise HTTPException(status_code=404, detail="Task not found")
from fastapi import FastAPI, HTTPException, Depends, Form, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import sqlite3

# --- Database Setup ---
con = sqlite3.connect("tasks.db", check_same_thread=False)
cur = con.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    completed BOOLEAN,
    due_date TEXT,
    priority INTEGER,
    owner TEXT
)
""")
con.commit()

# --- FastAPI App ---
app = FastAPI()

# --- Auth Setup ---
SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #TBnote: OAuth2 scheme for token-based authentication, tokenUrl is the endpoint to get the token

# Test user
test_users_db = {
    "Tiaan": {"username": "Tiaan", "password": "test123"}
}

# --- JWT Helpers ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy() #TBnote: Copying the data to avoid modifying the original
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15)) 
    to_encode.update({"exp": expire}) 
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #TBnote: Decoding the JWT token to get the payload
        username: str | None = payload.get("sub") #TBnote: 'sub' is a standard claim in JWT for the subject (user identifier)
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

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

# --- Root ---
@app.get("/")
def root():
    return {"message": "Welcome to the Task App API "}

# --- Create Task ---
@app.post("/tasks/")
def create_task(
    title: str = Form(..., min_length=3, max_length=50),
    description: Optional[str] = Form(None, max_length=200),
    completed: Optional[bool] = Form(False),
    due_date: Optional[str] = Form(None),
    priority: Optional[int] = Form(1, ge=1, le=5),
    current_user: str = Depends(get_current_user)
):
    cur.execute(""" 
        INSERT INTO tasks (title, description, completed, due_date, priority, owner)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, completed, due_date, priority, current_user)) 
    con.commit()

    task_id = cur.lastrowid #TBnote: Get the ID of the newly created task
    return {"message": "Task added successfully", "task": {
        "id": task_id, "title": title, "description": description,
        "completed": completed, "due_date": due_date,
        "priority": priority, "owner": current_user
    }}

# --- List Tasks ---
@app.get("/tasks/")
def list_tasks(
    priority: Optional[int] = Query(None),
    completed: Optional[bool] = Query(None),
    current_user: str = Depends(get_current_user)
):
    query = "SELECT * FROM tasks WHERE owner = ?"
    params = (current_user,)

    if priority is not None: #TBnote: Filter by priority if provided (Adds to params tuple)
        params += (priority,)
    if completed is not None: #TBnote: Filter by completion status if provided (Adds to params tuple)
        params += (completed,)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()

    tasks = [{
        "id": r[0], "title": r[1], "description": r[2], 
        "completed": bool(r[3]), "due_date": r[4],
        "priority": r[5], "owner": r[6]
    } for r in rows]

    return {"tasks": tasks}

# --- Get Task ---
@app.get("/tasks/{task_id}")
def get_task(task_id: int, current_user: str = Depends(get_current_user)):
    cur.execute("SELECT * FROM tasks WHERE id = ? AND owner = ?", (task_id, current_user))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": {
        "id": row[0], "title": row[1], "description": row[2],
        "completed": bool(row[3]), "due_date": row[4],
        "priority": row[5], "owner": row[6]
    }}

# --- Update Task ---
@app.put("/tasks/{task_id}")
def update_task(#TBnote: Using Form for all fields to allow form-data submission
    task_id: int,
    title: Optional[str] = Form(None, min_length=3, max_length=50),
    description: Optional[str] = Form(None, max_length=200),
    completed: Optional[bool] = Form(None),
    due_date: Optional[str] = Form(None),
    priority: Optional[int] = Form(None, ge=1, le=5),
    current_user: str = Depends(get_current_user)
):
    cur.execute("SELECT * FROM tasks WHERE id = ? AND owner = ?", (task_id, current_user)) #TBnote: Get tasks from the current user , by ID
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    updated = { #TBnote: Create new dictonary and merge existing values with new ones if provided
        "title": title if title is not None else row[1],
        "description": description if description is not None else row[2],
        "completed": completed if completed is not None else row[3],
        "due_date": due_date if due_date is not None else row[4],
        "priority": priority if priority is not None else row[5]
    }
    #TBnote: Update the task in the database with the merged values, similar to create_task but with an UPDATE query
    cur.execute("""
        UPDATE tasks SET title=?, description=?, completed=?, due_date=?, priority=?
        WHERE id=? AND owner=?
    """, (updated["title"], updated["description"], updated["completed"], updated["due_date"], updated["priority"], task_id, current_user)) 
    con.commit()

    return {"message": "Task updated successfully", "task": {**updated, "id": task_id, "owner": current_user}} #TBnote: Double asterisk used for Merging dictionaries

# --- Delete Task ---
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: str = Depends(get_current_user)):
    cur.execute("DELETE FROM tasks WHERE id = ? AND owner = ?", (task_id, current_user))
    con.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

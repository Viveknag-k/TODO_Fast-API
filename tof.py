from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class Todo(BaseModel):
    task: str

app = FastAPI()

# Dictionary to store users and their passwords
users_db = {}

# Dictionary to store each user's TODO list
todos_db = {}

@app.post('/Sign_Up/')
async def sign_up(user: Login):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists!")
    users_db[user.username] = user.password
    todos_db[user.username] = []  # Initialize an empty TODO list for the user
    return "Signed up successfully!"

@app.post('/Sign_In/')
async def sign_in(user: Login):
    if user.username in users_db and users_db[user.username] == user.password:
        return "Valid credentials"
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get('/Show_Tasks/')
async def show_tasks(username: str):
    if username not in todos_db:
        raise HTTPException(status_code=400, detail="User not found!")
    return todos_db[username]

@app.post('/Add_Task/')
async def add_task(username: str, todo: Todo):
    if username not in todos_db:
        raise HTTPException(status_code=400, detail="User not found!")
    todos_db[username].append(todo.task)
    return "Task added successfully"

@app.delete('/Delete_Task/')
async def delete_task(username: str, task_name: str):
    if username not in todos_db:
        raise HTTPException(status_code=400, detail="User not found!")
    if task_name in todos_db[username]:
        todos_db[username].remove(task_name)
        return "Task deleted successfully"
    return "Task not found!"

    
    
    
    
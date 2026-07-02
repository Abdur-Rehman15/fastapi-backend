from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
 title: str
 done: bool = False
 
@app.post("/tasks")
def create_task(task: Task):
 return {"message": "created", "task": task}
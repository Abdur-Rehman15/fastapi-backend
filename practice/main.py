# Build-along: a Task API that lives in memory (a Python list) with create, list, and get-by-id endpoints.

from fastapi import FastAPI, status, HTTPException, Path
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

tasks_db = []


class Task(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=20, max_length=200)
    done: bool = False


class TaskResponse(Task):
    taskID: int = Field(gt=0)
    date_posted: datetime = Field(default_factory=datetime.now)


@app.post("/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def createTask(new_task: Task):

    task_data = new_task.model_dump()
    task_data.update({"taskID": len(tasks_db) + 1, "date_posted": datetime.now()})

    tasks_db.append(task_data)

    return task_data


@app.get("/tasks", response_model=list[TaskResponse])
def allTasks():
    return tasks_db


@app.get("/task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def search_task_by_ID(task_id: int = Path(gt=0)):
    for task in tasks_db:
        if task["taskID"] == task_id:
            return task

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

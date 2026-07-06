from sqlmodel import SQLModel, Field, create_engine, Session, select
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class TaskBase(SQLModel):
    title: str
    done: bool = False


class TaskCreate(TaskBase):
    pass

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TaskResponse(Task):
    message: str | None = None

class TaskRead(Task):
    pass

class TaskUpdate(SQLModel):
    title: str | None = None
    done: bool | None = None


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("Creating tables...")
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# create
@app.post("/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(new_task: TaskCreate, session: SessionDep) -> TaskResponse:
    db_task = Task.model_validate(new_task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    response_data = TaskResponse.model_validate(db_task)
    response_data.message = f"task created with ID {db_task.id}"

    return response_data


# update
@app.patch("/update-task/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, updated_task: TaskUpdate, session: SessionDep
) -> TaskResponse:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    updated = updated_task.model_dump(exclude_unset=True)

    for k, v in updated.items():
        setattr(db_task, k, v)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    response_data = TaskResponse.model_validate(db_task)
    response_data.message = f"task with ID {db_task.id} updated"

    return response_data


# read
@app.get("/tasks", response_model=list[TaskRead])
def read_tasks(session: SessionDep):
    statement = select(Task)
    tasks = session.exec(statement).all()

    return tasks


# delete
@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, session: SessionDep):
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    session.delete(db_task)
    session.commit()

    return {"message": f"task with ID:{db_task.id} deleted successfully"}

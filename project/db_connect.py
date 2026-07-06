from sqlmodel import SQLModel, Field, create_engine, Session
from fastapi import FastAPI, Depends
from typing import Annotated
import uvicorn
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
    pass


DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

print("Creating tables...")
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/task", response_model=TaskResponse)
def create_task(new_task: TaskCreate, session: SessionDep) -> TaskResponse:
    db_task = Task.model_validate(new_task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    print(f"task created with ID {db_task.id}")
    return db_task


# if __name__ == "__main__":
#     # Start the server properly using uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

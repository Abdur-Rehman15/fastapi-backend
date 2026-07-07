from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from fastapi import FastAPI, Depends, status
from pydantic import EmailStr
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class UserBase(SQLModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="user")


class TaskBase(SQLModel):
    title: str
    done: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="tasks")


class TaskRead(SQLModel):
    id: int
    title: str
    done: bool
    user_id: int | None


class TaskUpdate(SQLModel):
    title: str | None = None
    done: bool | None = None


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

print("Creating tables...")
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)


@app.post("/users", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: SessionDep) -> UserBase:
    new_user = User.model_validate(user_in)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.post("/tasks", response_model=TaskRead)
def create_task_for_user(
    task_in: TaskCreate, curr_user_id: int, session: SessionDep
) -> TaskRead:
    db_task = Task(title=task_in.title, done=task_in.done, user_id=curr_user_id)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

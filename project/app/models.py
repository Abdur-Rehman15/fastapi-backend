from sqlmodel import Field, Relationship
from schemas import TaskBase, UserBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="tasks")

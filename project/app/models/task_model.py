from sqlmodel import Field, Relationship
from schemas.task_schema import TaskBase

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="tasks")

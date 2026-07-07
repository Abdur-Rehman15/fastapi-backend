from sqlmodel import SQLModel

class TaskBase(SQLModel):
    title: str
    done: bool = False


class TaskCreate(TaskBase):
    pass


class TaskResponse(SQLModel):
    id: int
    title: str
    done: bool
    user_id: int | None


class TaskUpdate(SQLModel):
    title: str | None = None
    done: bool | None = None

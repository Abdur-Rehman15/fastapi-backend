from sqlmodel import SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


# ////////////////////////


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

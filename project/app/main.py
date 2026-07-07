from fastapi import FastAPI
from routers import users, tasks
from sqlmodel import SQLModel
from database.database import engine

app = FastAPI()


@app.on_event("startup")
def on_startup():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


app.include_router(users.router)
app.include_router(tasks.router)

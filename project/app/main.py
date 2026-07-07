from fastapi import FastAPI
from routers import users
from sqlmodel import SQLModel
from database import engine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

app.include_router(users.router)
# app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
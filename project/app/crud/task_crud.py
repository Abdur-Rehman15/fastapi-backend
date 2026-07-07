from sqlmodel import Session, select
from models.task_model import Task
from schemas.task_schema import TaskCreate, TaskUpdate


def get_task_by_id(session: Session, task_id: int):
    return session.get(Task, task_id)


def get_all_tasks(session: Session, user_id: int):
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()


def create_task(session: Session, user_id: int, task_in: TaskCreate):
    db_task = Task(title=task_in.title, done=task_in.done, user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def update_task(session: Session, task_id: int, updated_task: TaskUpdate):
    db_task = get_task_by_id(session, task_id)
    if db_task:
        updated = updated_task.model_dump(exclude_unset=True)
        for k, v in updated.items():
            setattr(db_task, k, v)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int):
    db_task = get_task_by_id(session, task_id)
    if db_task:
        session.delete(db_task)
        session.commit()
    return db_task

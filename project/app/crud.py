from sqlmodel import Session, select
from models import User, Task
from schemas import UserCreate, UserUpdate, TaskCreate, TaskUpdate


def get_user_by_id(session: Session, user_id: int):
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_all_users(session: Session):
    statement = select(User)
    return session.exec(statement).all()


def create_user(session: Session, user_in: UserCreate):
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=user_in.password,  # for now, without any hash
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, updated_user: UserUpdate):
    db_user = get_user_by_id(session, user_id)
    if db_user:
        updated = updated_user.model_dump(exclude_unset=True)
        if "password" in updated:
            updated["hashed_password"] = updated.pop("password")
        for k, v in updated.items():
            setattr(db_user, k, v)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int):
    user = get_user_by_id(session, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user


# //////////////////////////////


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

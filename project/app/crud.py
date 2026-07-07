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

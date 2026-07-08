from fastapi import HTTPException, status, APIRouter, Depends
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
import crud.user_crud as user_crud
from database.database import SessionDep
from models.user_model import User
from security.security import get_current_user

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: SessionDep):
    user = user_crud.get_user_by_username(session, user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists with this username",
        )

    return user_crud.create_user(session, user_in)


@router.patch(
    "/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def update_user(updated_user: UserUpdate,session: SessionDep, current_user: User = Depends(get_current_user)):
    db_task = user_crud.get_user_by_id(session, current_user.id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found with this ID",
        )

    return user_crud.update_user(session, current_user.id, updated_user)


@router.get(
    "/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def get_user(session: SessionDep, current_user: User = Depends(get_current_user)):
    db_task = user_crud.get_user_by_id(session, current_user.id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this ID doesnt exist",
        )

    return db_task


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: SessionDep, current_user: User = Depends(get_current_user)):
    deleted_user = user_crud.delete_user(session, current_user.id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user doesnt exist with this ID",
        )

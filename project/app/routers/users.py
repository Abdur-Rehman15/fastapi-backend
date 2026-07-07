from fastapi import HTTPException, status, APIRouter
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
import crud.user_crud as user_crud
from database.database import SessionDep

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
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def update_user(user_id: int, updated_user: UserUpdate, session: SessionDep):
    db_task = user_crud.get_user_by_id(session, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found with this ID",
        )

    return user_crud.update_user(session, user_id, updated_user)


@router.get(
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def get_user(user_id: int, session: SessionDep):
    db_task = user_crud.get_user_by_id(session, user_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this ID doesnt exist",
        )

    return db_task


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep):
    deleted_user = user_crud.delete_user(session, user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user doesnt exist with this ID",
        )

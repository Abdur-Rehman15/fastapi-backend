from fastapi import HTTPException, status, APIRouter, Depends
from schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from database.database import SessionDep
import crud.user_crud as user_crud
import crud.task_crud as task_crud
from security.security import hash_password, get_current_user
from models.user_model import User

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    user = user_crud.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )
    return task_crud.create_task(session, current_user.id, task_in)


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task(
    task_id: int, updated_task: TaskUpdate, session: SessionDep, current_user: User = Depends(get_current_user)
):
    user = user_crud.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    task = task_crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found with this ID"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="task doesnt belong to this user",
        )

    return task_crud.update_task(session, task_id, updated_task)


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
)
def get_tasks(session: SessionDep, current_user: User = Depends(get_current_user)):
    user = user_crud.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    return task_crud.get_all_tasks(session, current_user.id)


@router.delete(
    "/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    user = user_crud.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    task = task_crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found with this ID"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="task doesnt belong to this user",
        )

    task_crud.delete_task(session, task_id)

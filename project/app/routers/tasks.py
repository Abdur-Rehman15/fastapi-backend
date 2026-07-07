from fastapi import HTTPException, status, APIRouter
from schemas import TaskCreate, TaskResponse, TaskUpdate
from database import SessionDep
import crud

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task_in: TaskCreate, session: SessionDep):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )
    return crud.create_task(session, user_id, task_in)


@router.patch(
    "/users/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task(
    user_id: int, task_id: int, updated_task: TaskUpdate, session: SessionDep
):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found with this ID"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="task doesnt belong to this user",
        )

    return crud.update_task(session, task_id, updated_task)


@router.get(
    "/users/{user_id}/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
)
def get_tasks(user_id: int, session: SessionDep):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    return crud.get_all_tasks(session, user_id)


@router.delete(
    "/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(user_id: int, task_id: int, session: SessionDep):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found with this ID"
        )

    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found with this ID"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="task doesnt belong to this user",
        )

    crud.delete_task(session, task_id)

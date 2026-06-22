from fastapi import APIRouter, Depends ,status
from sqlalchemy.orm import Session
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.dependencies.database import get_db
from app.services.todo_service import (
    create_todo_service,
    get_todos_service,
    get_todo_service,
    update_todo_service,
    delete_todo_service
)
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter( tags=["Todos"])

# todos = []

# @router.post("/todos")
# def create_todo(todo: TodoCreate):
#     todos.append(todo)
#     return {
#         "message": "Todo created",
#         "data": todo
#     }

# @router.get("/todos")
# def get_todos():
#     return todos

# @router.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     return {
#         "todo_id": todo_id
#     }

@router.get("/search")
def search_todos(status: bool = False):
    return {
        "status": status
    }

@router.post("/todos", response_model=TodoResponse,status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_todo_service(
        todo=todo,
        db=db,
        current_user=current_user
    )

@router.get("/todos", response_model=list[TodoResponse])
def get_todos(
    completed: bool | None = None,
    title: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_todos_service(
        completed=completed,
        title=title,
        db=db,
        current_user=current_user
    )

@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_todo_service(
        todo_id=todo_id,
        db=db,
        current_user=current_user
    )

@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_todo_service(
        todo_id=todo_id,
        todo=todo,
        db=db,
        current_user=current_user
    )

@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_todo_service(
        todo_id=todo_id,
        db=db,
        current_user=current_user
    )
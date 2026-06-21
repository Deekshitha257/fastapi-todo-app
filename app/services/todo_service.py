from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.user import User


def create_todo_service(
    todo: TodoCreate,
    db: Session,
    current_user: User
):
    db_todo = Todo(
        title=todo.title,
        completed=todo.completed,
        user_id=current_user.id
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def get_todos_service(
    completed: bool | None,
    title: str | None,
    db: Session,
    current_user: User
):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if title is not None:
        query = query.filter(Todo.title.contains(title))

    todos = query.all()

    return todos


def get_todo_service(
    todo_id: int,
    db: Session,
    current_user: User
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


def update_todo_service(
    todo_id: int,
    todo: TodoUpdate,
    db: Session,
    current_user: User
):
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )

    if not db_todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db_todo.title = todo.title
    db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo_service(
    todo_id: int,
    db: Session,
    current_user: User
):
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )

    if not db_todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(db_todo)

    db.commit()

    return {
        "message": "Todo deleted successfully"
    }
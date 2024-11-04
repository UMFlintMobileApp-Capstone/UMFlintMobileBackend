from fastapi import APIRouter,Depends
from app.db.db import session
from app.db.models import Todo
from app.core.auth import get_logged_user
from fastapi_sso.sso.base import OpenID

router = APIRouter()

@router.post("/test/create")
async def create_todo(text: str, is_complete: bool = False):
    test = Todo(text=text, is_done=is_complete)
    session.add(test)
    session.commit()
    return {"todo added": test.text}

@router.get("/test/")
async def get_all_todos():
    todos_query = session.query(Todo)
    return todos_query.all()

@router.get("/test/done")
async def list_done_todos():
    todos_query = session.query(Todo)
    done_todos_query = todos_query.filter(Todo.is_done==True)
    return done_todos_query.all()

@router.put("/test/update/{id}")
async def update_todo(
    id: int,
    new_text: str = "",
    is_complete: bool = False
):
    todo_query = session.query(Todo).filter(Todo.id==id)
    todo = todo_query.first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    session.add(todo)
    session.commit()

@router.delete("/test/delete/{id}")
async def delete_todo(id: int):
    todo = session.query(Todo).filter(Todo.id==id).first() # Todo object
    session.delete(todo)
    session.commit()
    return {"todo deleted": todo.text}

@router.get("/protected")
async def protected_endpoint(user: OpenID = Depends(get_logged_user)):
    """This endpoint will say hello to the logged user.
    If the user is not logged, it will return a 401 error from `get_logged_user`."""
    return {
        "message": f"Hello, {user.email}!",
    }
from fastapi import APIRouter,Depends
from app.db.db import session
from app.db.models import Todo
from app.core.auth import get_logged_user
from fastapi_sso.sso.base import OpenID

""" 
app/routers/test.py:

This is a test route that we can remove once we don't
need it anymore.

It's a basic task management tool depending on the user 
being logged in.

You create a router by using:
    router = APIRouter()

Then you can create a route by:
    @router.{GET/POST/PUT/DELETE}("SLUG")
    async def SLUG(PARAMETERS):
        return JSON_OBJECT

If you want authorization dependency, just add the
parameter:
    user: OpenID = Depends(get_logged_user)

And there you can then call user to get the user's 
information.
"""

router = APIRouter()

@router.post("/test/create")
async def create_todo(text: str, is_complete: bool = False, user: OpenID = Depends(get_logged_user)):
    test = Todo(text=text, is_done=is_complete)
    session.add(test)
    session.commit()
    return {"todo added": test.text}

@router.get("/test/")
async def get_all_todos(user: OpenID = Depends(get_logged_user)):
    todos_query = session.query(Todo)
    return todos_query.all()

@router.get("/test/done")
async def list_done_todos(user: OpenID = Depends(get_logged_user)):
    todos_query = session.query(Todo)
    done_todos_query = todos_query.filter(Todo.is_done==True)
    return done_todos_query.all()

@router.put("/test/update/{id}")
async def update_todo(
    id: int,
    new_text: str = "",
    is_complete: bool = False,
    user: OpenID = Depends(get_logged_user)
):
    todo_query = session.query(Todo).filter(Todo.id==id)
    todo = todo_query.first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    session.add(todo)
    session.commit()

@router.delete("/test/delete/{id}")
async def delete_todo(id: int, user: OpenID = Depends(get_logged_user)):
    todo = session.query(Todo).filter(Todo.id==id).first() # Todo object
    session.delete(todo)
    session.commit()
    return {"todo deleted": todo.text}
from fastapi import APIRouter
from app.db.db import session
from app.db.models import Todo

""" 
<app/routers/test.py>

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

# create the router
router = APIRouter()

# create task via POST
@router.post("/test/create")
async def create_todo(text: str, is_complete: bool = False):
    # create an instance of the Todo class
    test = Todo(text=text, is_done=is_complete)

    # add the instance to database and commit it to the database
    session.add(test)
    session.commit()

    # return a value
    return {"todo added": test.text}

@router.get("/test/")
async def get_all_todos():
    # query all Todos in the database
    todos_query = session.query(Todo)

    # return all
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
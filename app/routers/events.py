from fastapi import APIRouter,Depends
from app.db.db import session
from app.db.models import Todo
from app.core.auth import get_logged_user
from fastapi_sso.sso.base import OpenID

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

router = APIRouter()

@router.get("/events/testing")
async def testing(user: OpenID = Depends(get_logged_user)):
    events_query = session.query(Events)

    return events_query.all()
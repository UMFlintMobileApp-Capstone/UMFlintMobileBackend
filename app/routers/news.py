from fastapi import APIRouter,Depends
from fastapi_sso.sso.base import OpenID
import app.core.umich_api as api
import app.db.db as db

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

## get for news items, ignoring our database aspect for now
## how that is done needs to be determined by how we display things
## suggestion: maybe we only return maximum of 5-6 results period, umich returns 4 currently
## we can get the other 1-2 from our database (select top 2 desc)
@router.get("/news/items")
async def items():
    return api.get_news_items()


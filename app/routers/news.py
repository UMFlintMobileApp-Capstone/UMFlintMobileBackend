from fastapi import APIRouter
from app.core.data_process import get_all_news

""" 
<app/routers/news.py>

"""

router = APIRouter()

## get for news items, ignoring our database aspect for now
## how that is done needs to be determined by how we display things
## suggestion: maybe we only return maximum of 5-6 results period, umich returns 4 currently
## we can get the other 1-2 from our database (select top 2 desc)
@router.get("/news/get/{items}")
async def items(items):
    return get_all_news(items)
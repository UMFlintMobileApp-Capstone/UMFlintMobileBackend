from fastapi import APIRouter,Depends
from fastapi_sso.sso.base import OpenID
from app.core.umich_api import get_news_items
from app.db.db import session
from app.db.models import News
from datetime import datetime

""" 
<app/routers/news.py>

"""

router = APIRouter()

## get for news items, ignoring our database aspect for now
## how that is done needs to be determined by how we display things
## suggestion: maybe we only return maximum of 5-6 results period, umich returns 4 currently
## we can get the other 1-2 from our database (select top 2 desc)
@router.get("/news/get/{items}")
def items(items):
    articles = []

    for article in get_news_items():
        articles.append(article)

    for article in session.query(News).all():

        articles.append(
            {
                'id': article.id,
                'title': article.title,
                'url': article.url,
                'publication_date': article.publication_date,
                'excerpt':article.excerpt,
                'image_url': article.image_url,
                'author': {
                    'name': article.author_name,
                    'email': article.author_email
                }
            }
        )


    articles.sort(key=lambda d: datetime.strptime(d['publication_date'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
    if(items.isnumeric()):
        return articles[:int(items)]
    else:
        return articles


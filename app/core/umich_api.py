import requests as r

async def get_news_items():
    return r.get("https://news.umflint.edu/wp-json/umf/v2/posts").json

def get_announcement_items():
    return r.get('https://www.umflint.edu/wp-json/wp-content-types/announcements').json()
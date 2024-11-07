import requests as r

async def get_news_items():
    return r.get("https://news.umflint.edu/wp-json/umf/v2/posts").json

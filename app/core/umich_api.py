import requests as r

def get_news_items():
    return r.get("https://news.umflint.edu/wp-json/umf/v2/posts").json()

def get_announcement_items():
    return r.get('https://www.umflint.edu/wp-json/wp-content-types/announcements').json()

def get_events_items():
    return r.get("https://events.umflint.edu/api/events/promoted-feed").json()

def get_events_groups():
    return r.get("https://events.umflint.edu/api/wp-block/groups/all").json()

def get_academic_events():
    return r.get("https://www.umflint.edu/registrar/wp-json/wp-content-types/academic-events/current").json()
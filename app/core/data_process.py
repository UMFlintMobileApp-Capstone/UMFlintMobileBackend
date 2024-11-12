from app.core.umich_api import *
from app.core.db_access import *
from datetime import datetime

# this will return the combination of announcement items from the db and api
def get_announcement_items(items):
    # create a list of all announcements
    allAnnouncements=[]

    # get announcements from api and iterate
    for announcement in get_announcement_items()['data']:
        # some clean up for getting the start date (some only have publish at)
        if announcement['display_start']!="":
            dateStart = announcement['display_start']
        else:
            dateStart = announcement['published_at']

        # get all the roles
        roles = []
        for role in announcement['affiliations']:
            roles.append({'role': getRoleId(role['name'])})

        # create a dictionary of an individual announcement
        announcementJson = {
                    'id': announcement['id'],
                    'title': announcement['title'],
                    'description':announcement['description'],
                    'dateStart': dateStart,
                    'dateEnd': announcement['display_end'],
                    'roles': roles
                }

        # add the dictionary to the list
        allAnnouncements.append(announcementJson)

        # get from the database, iterate for each
    for announcement in get_announcements():
        # get all the roles (and since it's comma seperated, iterate)
        roles = []
        for role in announcement.role.split(","):
            roles.append({'role': role})

        # create a dictionary of an individual announcement
        announcementJson = {
                    'id': announcement.id,
                    'title': announcement.title,
                    'description':announcement.description,
                    'dateStart': announcement.dateStart,
                    'dateEnd': announcement.dateEnd,
                    'roles': roles
                }

        # add the dictionary to the list
        allAnnouncements.append(announcementJson)

    # sort by newest start date
    allAnnouncements.sort(key=lambda d: datetime.strptime(d['dateStart'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    # if the query is a number, return by a max number of items, otherwise all
    if(items.isnumeric()):
        return allAnnouncements[:int(items)]
    else:
        return allAnnouncements


# return combined news items from db and api
def get_news_items(items):
    articles = []

    # get api news items
    for article in get_news_items():
        articles.append(article)

    # get db news items
    for article in get_news():
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

    # sort by pub date desc
    articles.sort(key=lambda d: datetime.strptime(d['publication_date'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
    # return top *items* else all
    if(items.isnumeric()):
        return articles[:int(items)]
    else:
        return articles


# based on the name, give a role id to match database
def getRoleId(name):
    if name=="student":
        return 1
    elif name=="staff":
        return 2
    elif name=="faculty":
        return 3
    else:
        return 0
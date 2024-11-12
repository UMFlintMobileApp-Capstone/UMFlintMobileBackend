from fastapi import HTTPException
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from app.db.db import session
from app.db.models import User

"""
<app/core/auth.py>

This is the core authorization script that sets up the Google OAUTH SSO.

Include this script to get access to the getUserDetails function that will
give the ability to see if a user is logged in and what their details are
based on their JWT (as provided by Google).

getUserDetails will create the user if they do not exist, otherwise it'll
just return the user's details. On the case of an invalid JWT token it'll
forcibly raise a 403 unauthorized with the details.
"""

def getUserDetails(token: str):
    try:
        # use google's oauth verification
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            os.getenv('GOOGLE_CLIENT_ID')
        )

        # we only want our specific domain, raise 403 if not correct
        if idinfo['hd'] != os.getenv('GOOGLE_AUTHORIZED_DOMAIN'):
            raise HTTPException(status_code=403, detail="Invalid domain credentials")

        # try to find an existing user, if none the orm raises an exception
        # if they exist, just return the user information
        try:
            user = session.query(User).filter_by(id = idinfo['sub']).one()
            return user
        except:
            # let's create the user then and return the user information
            user = User(
                id=idinfo['sub'],
                email=idinfo['email'],
                firstname=idinfo['given_name'],
                surname=idinfo['family_name'],
                role=1
            )
            session.add(user)
            session.commit()
            return user

    # this is assuming correct domain but for some reason invalid credentials
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid credentials")
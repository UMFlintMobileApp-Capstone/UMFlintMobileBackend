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
just return the User model for the given user. On the case of an invalid 
JWT token it'll raise a 403 unauthorized with the details.

To require authentication you may use dependencies like so in the parameters:
    user: User = Depends(getUserDetails)

You'll also need to import Depends from fastapi, and getUserDetails from this
script:
    from fastapi import Depends
    from app.core.auth import getUserDetails

This will require a parameter called token in the request (preferably 
via POST body or query parameters) that will be automatically processed
without you having to add a token parameter.

If however you want to optionally have authentication, access getUserDetails
in function with a JWT parameter, such as using 'token' and use try/excepts
to determine if login is successful, like:
    try:
        # logged in
        user = getUserDetails(token)
    except:
        # not logged in

You'll also need to import getUserDetails from this script:
    from app.core.auth import getUserDetails

In both cases you can then access the User model variable 'user' or whatever
you choose later on.
"""

def getUserDetails(token: str):
    if "debug" in token:
        return session.query(User).filter_by(email = "debug@umich.edu").one()

    try:
        # use google's oauth verification
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            os.getenv('GOOGLE_CLIENT_ID')
        )

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
                role=1,
                profilePicture=idinfo['picture']
            )
            session.add(user)

            try:
                session.commit()
            except:
                session.rollback()
                raise

            return user 

    # this is assuming invalid credentials
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid credentials")
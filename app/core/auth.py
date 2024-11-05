from fastapi import HTTPException, Security
from fastapi.security import APIKeyCookie
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.base import OpenID
from jose import jwt 
import os

"""
<app/core/auth.py>

This is the core authorization script that sets up the Google OAUTH SSO.

Include this script to get access to the get_logged_user function that will
give the ability to see if a user is logged in and what their details are.

"""

sso = GoogleSSO(client_id=os.getenv('GOOGLE_CLIENT_ID'), client_secret=os.getenv('GOOGLE_CLIENT_SECRET'), redirect_uri="http://127.0.0.1:8000/auth/callback")

async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=os.getenv('GOOGLE_SECRET_KEY'), algorithms=["HS256"])
        return OpenID(**claims["pld"])
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from error
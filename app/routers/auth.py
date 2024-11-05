from fastapi import APIRouter, Depends, HTTPException, Request
import datetime
from fastapi.responses import RedirectResponse
from jose import jwt
from app.core.auth import sso, get_logged_user
import os
from fastapi_sso.sso.base import OpenID

"""
<app/routers/auth.py>

This is the authentication route that handles managing 
user authorization such as login, logout, etc.

"""

router = APIRouter()

@router.get("/auth/login")
async def login():
    """Redirect the user to the Google login page."""
    async with sso:
        return await sso.get_login_redirect()


@router.get("/auth/logout")
async def logout():
    """Forget the user's session."""
    response = RedirectResponse(url="/")
    response.delete_cookie(key="token")
    return response


@router.get("/auth/callback")
async def login_callback(request: Request):
    """Process login and redirect the user to the protected endpoint."""
    async with sso:
        openid = await sso.verify_and_process(request)
        if not openid:
            raise HTTPException(status_code=401, detail="Authentication failed")
    # Create a JWT with the user's OpenID
    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({"pld": openid.dict(), "exp": expiration, "sub": openid.id}, key=os.getenv('GOOGLE_SECRET_KEY'), algorithm="HS256")
    response = RedirectResponse(url="/auth/success")
    response.set_cookie(
        key="token", value=token, expires=expiration
    )
    return response

@router.get("/auth/success")
async def login_success(user: OpenID = Depends(get_logged_user)):
    """This endpoint will say hello to the logged user.
    If the user is not logged, it will return a 401 error from `get_logged_user`."""
    return {
        "message": f"Hello, {user.email}!",
    }
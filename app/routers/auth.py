from fastapi import APIRouter
from app.core.auth import getUserDetails

"""
<app/routers/auth.py>

This is the authentication route that handles managing 
user authorization.

"""

router = APIRouter()

@router.post("/auth/callback")
def login_app_callback(token: str):
    user = getUserDetails(token)

    return {
        'status': 'success',
        'message': f'Logged in with user: {user.email}'
    }
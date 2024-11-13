from fastapi import APIRouter
from app.core.auth import getUserDetails
from app.db.models import User
from app.db.db import session

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

@router.get("/debug/create")
def debugCreateUser(email: str):
    # DO NOT KEEP THIS ROUTE, ONLY FOR TEST
    user = User(
            email=email,
            firstname=email.split("@")[0],
            surname="user",
            role=1,
            profilePicture=""
        )
    session.add(user)
    session.commit()
    return user

from fastapi import APIRouter, Depends
from app.db.models import User
from app.core.auth import getUserDetails
from fastapi import APIRouter
from app.core.db_access import getUserByEmail, getUserById, getUsers

""" 
<app/routers/user.py>

"""

# create the router
router = APIRouter()

@router.get("/user/byId/{id}")
def getUserId(id: int, user: User = Depends(getUserDetails)):
    return getUserById(id)

@router.get("/user/byEmail/{email}")
def getUserEmail(email: str, user: User = Depends(getUserDetails)):
    return getUserByEmail(email)

@router.get("/users")
def getUser(user: User = Depends(getUserDetails)):
    return getUsers()
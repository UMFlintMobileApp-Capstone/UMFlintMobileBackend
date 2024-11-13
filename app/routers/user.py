from fastapi import APIRouter, Depends
from app.db.db import session
from app.db.models import User
from app.core.auth import getUserDetails
from fastapi import APIRouter

""" 
<app/routers/user.py>

"""

# create the router
router = APIRouter()

@router.get("/user/byId/{id}")
def getUserById(id: int, user: User = Depends(getUserDetails)):
    return session.query(User).filter(User.id==id).all()

@router.get("/user/byEmail/{email}")
def getUserByEmail(email: str, user: User = Depends(getUserDetails)):
    return session.query(User).filter(User.email==email).all()
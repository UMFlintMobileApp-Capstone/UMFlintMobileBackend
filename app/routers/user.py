from fastapi import APIRouter
from app.db.db import session
from app.db.models import User
from app.core.auth import getUserDetails
from fastapi import APIRouter

""" 
<app/routers/user.py>

"""

# create the router
router = APIRouter()

@router.get("/user/{id}")
def getUser(id: int, token: str):
    getUserDetails(token)
    
    return session.query(User).filter(User.id==id).all()
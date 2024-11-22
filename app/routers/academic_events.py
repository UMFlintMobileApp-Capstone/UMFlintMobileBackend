from fastapi import APIRouter
from app.core.umich_api import get_academic_events


router = APIRouter()

@router.get("/acadevents/get")
def getAcademicEvents():
    return get_academic_events()

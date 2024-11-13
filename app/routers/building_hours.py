from fastapi import APIRouter
from app.core.db_access import get_hours

"""
<app/routers/building_hours.py>

Getter for the building hours

Each element contains the building name, open time, and close time
"""
router = APIRouter()

@router.get("/hours/get")
def getHours():
    return get_hours()


"""
class BuildingHours(Base):
    __tablename__ = "Building Hours"

    building = Column(String, primary_key=True)
    open_at = Column(DateTime)
    close_at = Column(DateTime)
"""
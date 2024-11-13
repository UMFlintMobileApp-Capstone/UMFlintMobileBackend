from fastapi import APIRouter
from app.core.db_access import get_maps

"""
<app/routers/maps.py>

Getter for collecting every map from the PostgresDB

Each map elements contains an id, building name, floor number, and map image (unknwon format as of right now)
"""

router = APIRouter()

@router.get("/maps/get")
def getMaps():
    return get_maps()


"""
class Maps(Base):
    __tablename__ = "Maps"

    id = Column(Integer, primary_key=True)
    building_name = Column(String)
    floor_num = Column(Integer)
    map_img = Column(String)
"""
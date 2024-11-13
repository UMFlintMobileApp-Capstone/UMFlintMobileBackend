from fastapi import APIRouter, Depends
from app.db.db import session
from app.db.models import Schedule, Scheduling, User, Messages, Threads
from app.core.auth import getUserDetails
from app.core.db_access import getUserByEmail
from sqlalchemy import desc
import uuid

"""
<app/routers/schedule.py>

"""

# create the router
router = APIRouter()

@router.get("/schedule/student")
async def getStudentMeetingSchedules(user: User = Depends(getUserDetails)):
    meetings = []

    # get all meetings for the current user
    for meeting in session.query(
                Schedule, Scheduling
            ).filter(
                Schedule.user==user.email,
                Schedule.uuid == Scheduling.uuid
            ).all():
        
        schedule = meeting[0]
        scheduling = meeting[1]

        users = []

        # get all users for a given meeting
        for u in session.query(Schedule).filter(Schedule.uuid==schedule.uuid).all():
            users.append({"user": getUserByEmail(u.user), "accepted": u.accepted}) 

        # form dict and add to list
        meetings.append({
            "uuid": scheduling.uuid,
            "type": scheduling.type,
            "title": scheduling.title,
            "notes": scheduling.notes,
            "date": scheduling.date,
            "scheduler": scheduling.scheduler,
            "threadUuid": scheduling.threadUuid,
            "users": users
            }
        )
    
    # return all meetings
    return {"meetings": meetings}

@router.post("/schedule/student")
async def addStudentMeeting(title: str, notes: str, date: str, users: str, user: User = Depends(getUserDetails)):
    tId = uuid.uuid4()
    mId = uuid.uuid4()

    session.add(
        Scheduling(
            uuid = mId,
            type = "student",
            title = title,
            threadUuid = tId,
            date = date,
            scheduler = user.email
        )
    )

    session.add(
        Schedule(
            uuid = mId,
            user = user.email,
            accepted = True
        )
    )
    session.add(
        Threads(
            uuid = tId,
            user = user.email
        )
    )

    for u in users.split(","):
        session.add(
            Schedule(
                uuid = mId,
                user = u,
                accepted = False
            )
        )
    
    session.commit()
    return {"status": "success", "message": "Sucessfully added new meeting!"}

@router.post("/schedule/student/status")
async def setStatusStudentMeeting(meeting: str, accept: bool, user: User = Depends(getUserDetails)):
    if accept:
        meeting = session.query(
            Schedule, Scheduling
        ).filter(
            Schedule.user==user.email,
            Scheduling.uuid==Schedule.uuid
        ).first()

        schedule = meeting[0]
        scheduling = meeting[1]

        schedule.accepted = True

        session.add(
            Threads(
                uuid = scheduling.threadUuid,
                user = user.email
            )
        )
        session.add(schedule)

        session.commit()
        return {"status": "success", "message": "Accepted meeting!"}
    else:
        session.delete(
            session.query(Schedule).filter(Schedule.user==user.email)
        )

        session.commit()
        return {"status": "success", "message": "Declined meeting!"}

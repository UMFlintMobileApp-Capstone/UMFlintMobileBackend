from fastapi import APIRouter, Depends, Response
from app.db.db import session
from app.db.models import Schedule, Scheduling, User, Locations, Threads, Advisors, Degrees, Colleges, AdvisorLinks, AdvisorAvailabilities, RoomAvailabilities
from app.core.auth import getUserDetails
from app.core.db_access import getUserByEmail
import uuid
from ics import Calendar, Event, Attendee

"""
<app/routers/schedule.py>

Handles scheduling meetings between students, advisor meetings, and room booking.

Student:
    - Group or Individual
    - Automatically creates a chat thread
    - Invite, seperate route for accepting invite

Advisor:
    - One-to-one
    - Availabilities

Room:
    - Group or Individual
    - Availabilities
    - Locations

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
                Schedule.uuid == Scheduling.uuid,
                Scheduling.type == "student"
            ).all():

        users = []

        # get all users for a given meeting
        for u in session.query(Schedule).filter(Schedule.uuid==meeting[0].uuid).all():
            users.append({"user": getUserByEmail(u.user), "accepted": u.accepted}) 

        location = session.query(Locations).filter(Locations.id==meeting[1].location).first()

        # form dict and add to list
        meetings.append({
            "uuid": meeting[1].uuid,
            "type": meeting[1].type,
            "title": meeting[1].title,
            "notes": meeting[1].notes,
            "location": {
              "name": location.name,
              "building": location.building,
              "address": location.address  
            },
            "startDate": meeting[1].startDate,
            "endDate": meeting[1].endDate,
            "scheduler": meeting[1].scheduler,
            "threadUuid": meeting[1].threadUuid,
            "users": users
            }
        )
    
    # return all meetings
    return {"meetings": meetings}

@router.get("/schedule/advisor")
async def getAdvisorMeetings(user: User = Depends(getUserDetails)):
    meetings = []

    # get all meetings for the current user
    for meeting in session.query(
                Schedule, Scheduling
            ).filter(
                Schedule.user==user.email,
                Schedule.uuid == Scheduling.uuid,
                Scheduling.type == "advisor"
            ).all():

        users = []

        # get all users for a given meeting
        for u in session.query(Schedule).filter(Schedule.uuid==meeting[0].uuid).all():
            users.append({"user": getUserByEmail(u.user), "accepted": u.accepted}) 

        location = session.query(Locations).filter(Locations.id==meeting[1].location).first()

        # form dict and add to list
        meetings.append({
            "uuid": meeting[1].uuid,
            "type": meeting[1].type,
            "title": meeting[1].title,
            "notes": meeting[1].notes,
            "location": {
              "name": location.name,
              "building": location.building,
              "address": location.address  
            },
            "startDate": meeting[1].startDate,
            "endDate": meeting[1].endDate,
            "scheduler": meeting[1].scheduler,
            "users": users
            }
        )
    
    # return all meetings
    return {"meetings": meetings}

@router.get("/schedule/room")
async def getRoomMeetings(user: User = Depends(getUserDetails)):
    meetings = []

    # get all meetings for the current user
    for meeting in session.query(
                Schedule, Scheduling
            ).filter(
                Schedule.user==user.email,
                Schedule.uuid == Scheduling.uuid,
                Scheduling.type == "room"
            ).all():

        users = []

        # get all users for a given meeting
        for u in session.query(Schedule).filter(Schedule.uuid==meeting[0].uuid).all():
            users.append({"user": getUserByEmail(u.user), "accepted": u.accepted}) 

        location = session.query(Locations).filter(Locations.id==meeting[1].location).first()

        # form dict and add to list
        meetings.append({
            "uuid": meeting[1].uuid,
            "type": meeting[1].type,
            "title": meeting[1].title,
            "notes": meeting[1].notes,
            "location": {
              "name": location.name,
              "building": location.building,
              "address": location.address  
            },
            "startDate": meeting[1].startDate,
            "endDate": meeting[1].endDate,
            "scheduler": meeting[1].scheduler,
            "users": users
            }
        )
    
    # return all meetings
    return {"meetings": meetings}

@router.post("/schedule/student")
async def addStudentMeeting(title: str, notes: str, startTime: str, endTime: str, location: int, users: str, user: User = Depends(getUserDetails)):
    tId = uuid.uuid4()
    mId = uuid.uuid4()

    session.add(
        Scheduling(
            uuid = mId,
            type = "student",
            title = title,
            notes = notes,
            location = location,
            threadUuid = tId,
            startDate = startTime,
            endDate = endTime,
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

@router.post("/schedule/advisor")
async def addAdvisorMeeting(reason: str, startTime: str, endTime: str, location: int, advisor: str, user: User = Depends(getUserDetails)):
    mId = uuid.uuid4()
    
    session.add(
        Scheduling(
            uuid = mId,
            type = "advisor",
            title = user.firstname+" "+user.surname+"'s Advisor Meeting",
            notes = reason,
            location = location,
            startDate = startTime,
            endDate = endTime,
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
        Schedule(
            uuid = mId,
            user = advisor,
            accepted = True
        )
    )
    
    session.commit()
    return {"status": "success", "message": "Sucessfully scheduled advisor meeting!"}

@router.post("/schedule/room")
async def addRoomScheduling(startTime: str, endTime: str, location: int, users: str, user: User = Depends(getUserDetails)):
    mId = uuid.uuid4()
    
    session.add(
        Scheduling(
            uuid = mId,
            type = "room",
            title = user.firstname+" "+user.surname+"'s Room Booking",
            location = location,
            startDate = startTime,
            endDate = endTime,
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

    for u in users.split(","):
        session.add(
            Schedule(
                uuid = mId,
                user = u,
                accepted = False
            )
        )
    
    session.commit()
    return {"status": "success", "message": "Sucessfully scheduled room!"}

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

@router.get("/schedule/locations")
async def getSchedulingLocations(user: User = Depends(getUserDetails)):
    return session.query(
            Locations
        ).all()

@router.get("/schedule/colleges")
async def getSchedulingColleges(user: User = Depends(getUserDetails)):
    return session.query(
            Colleges
        ).all()

@router.get("/schedule/college/{college}/degrees")
async def getSchedulingDegrees(college: int, user: User = Depends(getUserDetails)):
    return session.query(
            Degrees
        ).filter(
            Degrees.collegeId==college
        ).all()

@router.get("/schedule/college/{college}/degree/{degree}/advisors")
async def getSchedulingAdvisors(college: int, degree: int, user: User = Depends(getUserDetails)):
    return session.query(
            Advisors
        ).filter(
            AdvisorLinks.college==college, AdvisorLinks.degree==degree
        ).join(
            AdvisorLinks, AdvisorLinks.advisor==Advisors.id
        ).all()

@router.get("/schedule/advisor/{advisor}/availabilities")
async def getSchedulingAdvisorsAvailabilities(advisor: int, user: User = Depends(getUserDetails)):
    return session.query(
            AdvisorAvailabilities
        ).filter(
            AdvisorAvailabilities.advisor==advisor,
            AdvisorAvailabilities.startTime!=Scheduling.startDate,
            AdvisorAvailabilities.endTime!=Scheduling.endDate
        ).join(
            Advisors, Advisors.id==advisor
        ).join(
            Schedule, Schedule.user==Advisors.email
        ).join(
            Scheduling, Scheduling.uuid==Schedule.uuid
        ).all()

@router.get("/schedule/room/{room}/availabilities")
async def getSchedulingRoomAvailabilities(room: int, user: User = Depends(getUserDetails)):
    return session.query(
        RoomAvailabilities
    ).filter(
        RoomAvailabilities.id==room,
        RoomAvailabilities.startTime!=Scheduling.startDate,
        RoomAvailabilities.endTime!=Scheduling.endDate
    ).join(
        Locations, Locations.id==RoomAvailabilities.id
    ).join(
        Scheduling, Scheduling.location == room
    ).all()

@router.get("/schedule/meeting/{id}/ical")
async def getiCalForMeeting(id: str, user: User = Depends(getUserDetails)):
    c = Calendar()
    e = Event()

    meeting = session.query(
            Schedule, Scheduling
        ).filter(
            Scheduling.uuid==id,
            Schedule.uuid==Scheduling.uuid,
            Schedule.user==user.email
        ).first()
    
    for u in session.query(Schedule).filter(Schedule.uuid==meeting[0].uuid, Schedule.accepted==True).all():
        e.add_attendee(Attendee(email=u.user))

    e.name = meeting[1].title
    e.begin = meeting[1].startDate
    e.end = meeting[1].endDate
    e.description = meeting[1].notes
    e.location = session.query(Locations).filter(Locations.id==meeting[1].location).first().name
    e.organizer = meeting[0].user

    c.events.add(e)

    # !! Bug currently where the time is assumed to be UTC even though it's Eastern
    # This is a problem with this ical library (ics) not supporting time zones
    # Need to either switch libraries or convert eastern to utc
    return Response(content=c.serialize(), media_type="text/calendar")


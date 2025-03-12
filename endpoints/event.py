from fastapi import APIRouter, Depends, HTTPException, Response, status
from db import Event, User
from auth import get_current_user, roles_checker
from data_validation import EventRequest
router = APIRouter()


@router.post("/events")
def create_event(request: EventRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Event(name=request.name, description=request.description, date=request.date, image=request.image).save()
        response = Response(status_code=status.HTTP_201_CREATED)
        return response
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/events")
def get_events():
    events = Event.objects.all()
    if events:
        return events
    return {"message": "No events"}

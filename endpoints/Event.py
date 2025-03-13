from fastapi import APIRouter, Depends, HTTPException, Response, status
from DB import Event, User
from Auth import get_current_user, roles_checker
from Data_validation import EventRequest
router = APIRouter()


@router.post("/events", tags=["Events"])
def create_event(request: EventRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Event(name=request.name, description=request.description, date=request.date, image=request.image).save()
        return {"message": "Event created"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete("/events", tags=["Events"])
def delete_event(name: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Event.objects(name=name).delete()
        return {"message": "Event deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/events", tags=["Events"])
def get_events():
    events = Event.objects.all()
    if events:
        return events
    return {"message": "No events"}

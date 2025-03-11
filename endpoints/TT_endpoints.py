from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user, roles_checker
from db import User, TimeTable
from data_validation import TimeTableRequest
router = APIRouter()


@router.post("/create_Timetable")
def create_tt(request: TimeTableRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        TimeTable(year=request.year, image=request.image).save()
        return {"message": "TimeTable created successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/delete_Timetable")
def delete_tt(year: int, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        if TimeTable.objects.filter(year=year).exists():
            TimeTable.objects.filter(year=year).delete()
            return {"message": "TimeTable deleted successfully"}
        raise HTTPException(status_code=404, detail="TimeTable not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/update_Timetable")
def update_tt(request: TimeTableRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        existing_tt = TimeTable.objects.first()
        if existing_tt:
            update = request.model_dump(exclude_unset=True)
            TimeTable.objects.update(update)
            return {"message": "TimeTable updated successfully"}
        raise HTTPException(status_code=404, detail="No existing TimeTable found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/get_Timetable")
def get_tt():
    return TimeTable.objects.all()

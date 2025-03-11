from auth import User, get_current_user, roles_checker
from fastapi import APIRouter, Depends, HTTPException
from db import Faculty
from data_validation import FacultyRequest
router = APIRouter()


@router.post("/create_faculty")
def create_faculty(request: FacultyRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Faculty(name=request.name, roll_no=request.roll_no, designation=request.designation, image=request.image).save()
        return {"message": "Faculty created successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/update_faculty")
def update_faculty(request: FacultyRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        request = request.model_dump(exclude_unset=True)
        Faculty.objects.update(request)
        return {"message": "Faculty updated successfully"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/delete_faculty")
def delete_faculty(roll_no: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        if Faculty.objects.filter(roll_no=roll_no).first():
            Faculty.objects.filter(roll_no=roll_no).delete()
            return {"message": "Faculty deleted successfully"}
        raise HTTPException(status_code=404, detail="Faculty not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/get_faculty")
def get_faculty():
    faculty = Faculty.objects.all()
    return faculty

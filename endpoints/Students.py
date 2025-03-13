from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from Data_validation import StudentRequest
from Auth import roles_checker, get_current_user
from DB import Student, User
router = APIRouter()


@router.post("/create_students", tags=["students"], response_model=StudentRequest)
def create_student(request: StudentRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Student(name=request.name, roll_no=request.roll_no, image=request.image).save()
        return {"message": "Student created successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/delete_student", tags=["students"])
def delete_student(roll_no: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        if Student.objects.filter(roll_no=roll_no).exists():
            Student.objects.filter(roll_no=roll_no).delete()
            return {"message": "Student deleted successfully"}
        raise HTTPException(status_code=404, detail="Student not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/get_students", tags=["students"])
def get_students():
    students = Student.objects.all().to_json()
    return JSONResponse(content=students)

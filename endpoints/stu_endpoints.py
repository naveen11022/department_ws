from fastapi import APIRouter, Depends, HTTPException
from data_validation import StudentRequest
from auth import roles_checker, get_current_user
from db import Student, User
router = APIRouter()


@router.post("/create_students")
def create_student(request: StudentRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Student(name=request.name, roll_no=request.roll_no, image=request.image).save()
        return {"message": "Student created successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/update_students")
def update_student(request: StudentRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        student_exists = Student.objects.filter(roll_no=request.roll_no).exists()

        if student_exists:
            update_data = request.model_dump(exclude_unset=True)

            Student.objects.filter(roll_no=request.roll_no).update(**update_data)

            return {"message": "Student updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/delete_student")
def delete_student(roll_no: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        if Student.objects.filter(roll_no=roll_no).exists():
            Student.objects.filter(roll_no=roll_no).delete()
            return {"message": "Student deleted successfully"}
        raise HTTPException(status_code=404, detail="Student not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/get_students")
def get_students():
    students = Student.objects.all()
    return students

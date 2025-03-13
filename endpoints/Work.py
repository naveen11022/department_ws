from fastapi import APIRouter, Depends, HTTPException
from Auth import roles_checker, get_current_user
from DB import User, Work
from Data_validation import WorkRequest
router = APIRouter()


@router.post("/works", tags=["Work"], response_model=WorkRequest)
def create_work(request: WorkRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Work(title=request.title, description=request.description, deadline=request.deadline, year=request.year).save()
        return {"message": "Work created"}
    raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/works", tags=["Work"])
def read_works():
    works = Work.objects.all()
    if not works:
        raise HTTPException(status_code=404, detail="Work not found")
    return {"works": works}

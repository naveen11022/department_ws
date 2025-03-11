from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from db import User, Notes
from auth import get_current_user, security, roles_checker
from mail_generate import send_mail
import os
directory = "pdf"
router = APIRouter()


@router.post("/notes")
def create_notes(year: int, subject: str, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file.filename)
        Notes(year=year, subject_code=subject, notes=file_path).save()
        with open(file_path, "wb") as f:
            content = file.file.read()
            f.write(content)
            f.close()
            send_mail(subject)
            return {"message": "Notes created successfully", "file_path": file_path}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/delete_notes")
def delete_notes(subject_code: str, current_user: User = Depends(security)):
    if roles_checker(current_user):
        note_entry = Notes.objects.filter(subject_code=subject_code).first()
        if not note_entry:
            raise HTTPException(status_code=404, detail="Notes not found")

        file_path = note_entry.notes
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

        Notes.objects.filter(subject_code=subject_code).delete()
        return {"message": "Notes deleted successfully"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/get_notes")
def get_notes(subject_code: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        notes = Notes.objects.filter(subject_code=subject_code)
        return notes


@router.get("/download_notes")
def download_notes(subject_code: str):
    note_entry = Notes.objects.filter(subject_code=subject_code).first()
    if not note_entry:
        raise HTTPException(status_code=404, detail="Notes not found")
    file_path = note_entry.notes
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=os.path.basename(file_path), media_type="application/octet-stream")

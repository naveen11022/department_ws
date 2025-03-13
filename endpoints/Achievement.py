from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from Data_validation import AchievementRequest
from DB import User, Achievement
from Auth import get_current_user, roles_checker
router = APIRouter()


@router.post("/achievement", tags=['achievement'])
def create_achievement(achievement: AchievementRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Achievement(Event_name=achievement.Event_name, level=achievement.level, organization=achievement.organization,
                    member=achievement.member, date=achievement.date, Overall=achievement.Overall,
                    event_image=achievement.event_image,
                    participation_image=achievement.participation_image).save()
        return {"message": "Achievement created successfully"}
    raise HTTPException(detail="Unauthorized", status_code=401)


@router.delete("/achievement", tags=["achievement"])
def delete_achievement(event_name: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        achievement = Achievement.objects.filter(level=event_name).first()
        if not achievement:
            raise HTTPException(status_code=404, detail="Achievement not found")
        achievement.delete()
        return {"message": "Achievement deleted successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/achievement_details", tags=["achievement"])
def get_achievement_details():
    achievements = Achievement.objects.all().to_json()
    return JSONResponse(content=achievements)

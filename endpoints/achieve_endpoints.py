from fastapi import APIRouter, Depends, HTTPException
from data_validation import AchievementRequest
from db import User, Achievement
from auth import get_current_user, roles_checker
router = APIRouter()


@router.post("/achievement")
def create_achievement(achievement: AchievementRequest, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        Achievement(level=achievement.level, organization=achievement.organization, member=achievement.member,
                    date=achievement.date, overall=achievement.Overall, event_image=achievement.event_image,
                    participation_image=achievement.participation_image).save()
        return {"message": "Achievement created successfully"}
    raise HTTPException(detail="Unauthorized", status_code=401)


@router.delete("/achievement")
def delete_achievement(event_name: str, current_user: User = Depends(get_current_user)):
    if roles_checker(current_user):
        achievement = Achievement.objects.filter(level=event_name).first()
        if not achievement:
            raise HTTPException(status_code=404, detail="Achievement not found")
        achievement.delete()
        return {"message": "Achievement deleted successfully"}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/achievement_details")
def get_achievement_details():
    achievement = Achievement.objects.findall()
    return achievement

from pydantic import BaseModel


class SignupRequest(BaseModel):
    username: str = None
    password: str = None


class FacultyRequest(BaseModel):
    name: str = None
    roll_no: str = None
    designation: str = None
    image: str = None


class StudentRequest(BaseModel):
    name: str = None
    roll_no: str = None
    image: str = None


class TimeTableRequest(BaseModel):
    year: int
    image: str = None


class AchievementRequest(BaseModel):
    level: str = None
    organization: str = None
    member: str = None
    date: str = None
    Overall: str = None
    event_image: str = None
    participation_image: str = None

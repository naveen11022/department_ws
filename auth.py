from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, APIRouter
from datetime import datetime, timezone, timedelta
from data_validation import SignupRequest
from db import User
from jwt import PyJWTError
import jwt
security = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = '-----'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 10
router = APIRouter()


def roles_checker(current_user: User):
    user = User.objects.filter(username=current_user.username).first()
    return user and user.role == "admin"


def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data["exp"] = expire.timestamp()
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_time = datetime.fromtimestamp(exp_timestamp, timezone.utc)
            if exp_time < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token has expired")

        user = User.objects.filter(username=payload["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/signup")
def user_signup(request: SignupRequest):
    user = User.objects.filter(username=request.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    User(username=request.username, password=request.password, role="user").save()
    return {"username": request.username, "details": "User created successfully"}


@router.post("/login")
def user_login(request: SignupRequest):
    user = User.objects.filter(username=request.username, password=request.password).first()
    if user:
        token = create_access_token(data={"username": request.username})
        return {"username": request.username, "message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

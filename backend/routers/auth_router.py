from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.services.auth.password_handler import hash_password, verify_password
from backend.services.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(data.password)
    new_user = User(
        email=data.email,
        hashed_password=hashed,
        full_name=data.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name
        }
    }

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return {
        "status": "success",
        "access_token": token,
        "token_type": "Bearer"
    }

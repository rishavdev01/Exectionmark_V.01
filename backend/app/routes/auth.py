"""
Auth route — POST /api/auth/login
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import users_collection

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    department: str
    avatar: str


@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    user = await users_collection.find_one({"email": body.email})
    if not user or user.get("password") != body.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return LoginResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        department=user["department"],
        avatar=user["avatar"],
    )

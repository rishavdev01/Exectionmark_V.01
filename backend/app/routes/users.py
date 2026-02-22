"""
Users route — CRUD + PAT update
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import users_collection

router = APIRouter()


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    department: str
    avatar: str
    github_pat: Optional[str] = None


class PATUpdate(BaseModel):
    github_pat: str


@router.get("")
async def get_users():
    users = []
    async for u in users_collection.find({}, {"_id": 0, "password": 0}):
        users.append(u)
    return users


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await users_collection.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/pat")
async def update_pat(user_id: str, body: PATUpdate):
    result = await users_collection.update_one(
        {"id": user_id}, {"$set": {"github_pat": body.github_pat}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "PAT updated"}

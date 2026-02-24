"""
Users route — CRUD + PAT update
Now reads from user_logins (single source of truth for all employees).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import users_collection

router = APIRouter()

# Fields to exclude from ALL user responses (never expose passwords)
_EXCLUDE = {"_id": 0, "organisation_password": 0, "employee_password": 0}


class PATUpdate(BaseModel):
    github_pat: str


@router.get("")
async def get_users():
    users = []
    async for u in users_collection.find({}, _EXCLUDE):
        users.append(u)
    return users


@router.get("/{user_id}")
async def get_user(user_id: str):
    # Support lookup by employee_id (primary key in user_logins)
    user = await users_collection.find_one({"employee_id": user_id}, _EXCLUDE)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
async def update_user(user_id: str, body: dict):
    body.pop("_id", None)
    body.pop("organisation_password", None)
    body.pop("employee_password", None)
    result = await users_collection.update_one(
        {"employee_id": user_id}, {"$set": body}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}


@router.put("/{user_id}/pat")
async def update_pat(user_id: str, body: PATUpdate):
    result = await users_collection.update_one(
        {"employee_id": user_id}, {"$set": {"github_pat": body.github_pat}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "PAT updated"}
